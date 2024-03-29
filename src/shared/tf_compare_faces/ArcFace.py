from tensorflow.python.keras.engine import training
import tensorflow
from tensorflow import keras

import os
from pathlib import Path
import gdown


def loadModel() -> keras.models.Model:
    """
    Load model
    :return: model
    """

    base_model = ResNet34()

    inputs = base_model.inputs[0]
    arcface_model = base_model.outputs[0]
    arcface_model = keras.layers.BatchNormalization(
        momentum=0.9,
        epsilon=2e-5,
    )(arcface_model)
    arcface_model = keras.layers.Dropout(0.4)(arcface_model)
    arcface_model = keras.layers.Flatten()(arcface_model)
    arcface_model = keras.layers.Dense(
        512, activation=None, use_bias=True, kernel_initializer="glorot_normal"
    )(arcface_model)
    embedding = keras.layers.BatchNormalization(
        momentum=0.9, epsilon=2e-5, name="embedding", scale=True
    )(arcface_model)
    model = keras.models.Model(inputs, embedding, name=base_model.name)

    # ---------------------------------------
    # check the availability of pre-trained weights

    home = str(Path.home())

    url = "https://drive.google.com/uc?id=1LVB3CdVejpmGHM28BpqqkbZP5hDEcdZY"
    file_name = "arcface_weights.h5"
    output = home + "/.deepface/weights/" + file_name
    Path(home + "/.deepface/weights/").mkdir(parents=True, exist_ok=True)

    if not os.path.isfile(output):
        print(file_name, " will be downloaded to ", output)
        gdown.download(url, output, quiet=False)

    # ---------------------------------------

    try:
        model.load_weights(output)
    except Exception as err:
        print("pre-trained weights could not be loaded.")
        print(
            "You might try to download it from the url ",
            url,
            " and copy to ",
            output,
            " manually",
        )
        print("Error: ", err)

    return model


def ResNet34() -> keras.models.Model:
    """
    ResNet-34 model architecture
    :return: model
    """
    img_input = tensorflow.keras.layers.Input(shape=(112, 112, 3))

    x = tensorflow.keras.layers.ZeroPadding2D(
        padding=1,
        name="conv1_pad",
    )(img_input)
    x = tensorflow.keras.layers.Conv2D(
        64,
        3,
        strides=1,
        use_bias=False,
        kernel_initializer="glorot_normal",
        name="conv1_conv",
    )(x)
    x = tensorflow.keras.layers.BatchNormalization(
        axis=3, epsilon=2e-5, momentum=0.9, name="conv1_bn"
    )(x)
    x = tensorflow.keras.layers.PReLU(
        shared_axes=[1, 2],
        name="conv1_prelu",
    )(x)
    x = stack_fn(x)

    model = training.Model(img_input, x, name="ResNet34")

    return model


def block1(
    x,
    filters,
    kernel_size: int = 3,
    stride: int = 1,
    conv_shortcut: bool = True,
    name: str = None,
) -> keras.layers.Layer:
    """
    A residual block

    :param x: input tensor
    :param filters: number of filters
    :param kernel_size: kernel size of middle conv layer at main path
    :param stride: stride at the first conv layer in the shortcut path
    :param conv_shortcut: whether to use convolution
                shortcut or identity shortcut
    :param name: name of the block
    :return: output tensor
    """

    bn_axis = 3

    if conv_shortcut:
        shortcut = tensorflow.keras.layers.Conv2D(
            filters,
            1,
            strides=stride,
            use_bias=False,
            kernel_initializer="glorot_normal",
            name=name + "_0_conv",
        )(x)
        shortcut = tensorflow.keras.layers.BatchNormalization(
            axis=bn_axis, epsilon=2e-5, momentum=0.9, name=name + "_0_bn"
        )(shortcut)
    else:
        shortcut = x

    x = tensorflow.keras.layers.BatchNormalization(
        axis=bn_axis, epsilon=2e-5, momentum=0.9, name=name + "_1_bn"
    )(x)
    x = tensorflow.keras.layers.ZeroPadding2D(
        padding=1,
        name=name + "_1_pad",
    )(x)
    x = tensorflow.keras.layers.Conv2D(
        filters,
        3,
        strides=1,
        kernel_initializer="glorot_normal",
        use_bias=False,
        name=name + "_1_conv",
    )(x)
    x = tensorflow.keras.layers.BatchNormalization(
        axis=bn_axis, epsilon=2e-5, momentum=0.9, name=name + "_2_bn"
    )(x)
    x = tensorflow.keras.layers.PReLU(
        shared_axes=[1, 2],
        name=name + "_1_prelu",
    )(x)

    x = tensorflow.keras.layers.ZeroPadding2D(
        padding=1,
        name=name + "_2_pad",
    )(x)
    x = tensorflow.keras.layers.Conv2D(
        filters,
        kernel_size,
        strides=stride,
        kernel_initializer="glorot_normal",
        use_bias=False,
        name=name + "_2_conv",
    )(x)
    x = tensorflow.keras.layers.BatchNormalization(
        axis=bn_axis, epsilon=2e-5, momentum=0.9, name=name + "_3_bn"
    )(x)

    x = tensorflow.keras.layers.Add(name=name + "_add")([shortcut, x])

    return x


def stack1(
    x,
    filters: int,
    blocks: int,
    stride1: int = 2,
    name: str = None,
) -> keras.layers.Layer:
    """
    A set of stacked residual blocks
    :param x: input tensor
    :param filters: number of filters
    :param blocks: number of blocks
    :param stride1: stride at the first conv layer of the first block
    :param name: name of the stack
    :return: output tensor
    """

    x = block1(x, filters, stride=stride1, name=name + "_block1")
    for i in range(2, blocks + 1):
        x = block1(
            x,
            filters,
            conv_shortcut=False,
            name=name + "_block" + str(i),
        )

    return x


def stack_fn(x: keras.layers.Layer) -> keras.layers.Layer:
    """
    Stack of residual blocks
    :param x: input tensor
    :return: output tensor
    """

    x = stack1(x, 64, 3, name="conv2")
    x = stack1(x, 128, 4, name="conv3")
    x = stack1(x, 256, 6, name="conv4")

    return stack1(x, 512, 3, name="conv5")
