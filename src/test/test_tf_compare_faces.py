from shared.tf_compare_faces.MatchFace import MatchFace
from shared.tf_compare_faces.KerasFace import KerasFace

import numpy as np
import warnings
warnings.filterwarnings("ignore")

match_face = MatchFace(euclidean_umbral=100, cosine_umbral=0.4)



class TestTf_compare_faces:
    def test_emb_and_emb(self):
        emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
        emb2 = KerasFace("/app/test/resources/robert_2.jpg").embedding
        d = match_face.compare(emb1, emb2)

        assert isinstance(d, tuple)
        assert isinstance(d[0], tuple)
        assert isinstance(d[1], tuple)
        assert isinstance(d[0][0], np.float32) or isinstance(d[0][0], np.float64)
        assert isinstance(d[1][0], np.float32) or isinstance(d[1][0], np.float64)
        assert d[0][1] == True
        assert d[1][1] == True

    def test_emb_and_path(self):
        emb1 = KerasFace("/app/test/resources/u/robert_1.jpg").embedding
        d = match_face.compare(emb1, 
                               "/app/test/resources/robert_2.jpg")

        assert isinstance(d, tuple)
        assert isinstance(d[0], tuple)
        assert isinstance(d[1], tuple)
        assert isinstance(d[0][0], np.float32) or isinstance(d[0][0], np.float64)
        assert isinstance(d[1][0], np.float32) or isinstance(d[1][0], np.float64)
        assert d[0][1] == True
        assert d[1][1] == True
    
    def test_path_and_path(self):
        d = match_face.compare("/app/test/resources/u/robert_1.jpg", 
                               "/app/test/resources/robert_2.jpg")

        assert isinstance(d, tuple)
        assert isinstance(d[0], tuple)
        assert isinstance(d[1], tuple)
        assert isinstance(d[0][0], np.float32) or isinstance(d[0][0], np.float64)
        assert isinstance(d[1][0], np.float32) or isinstance(d[1][0], np.float64)
        assert d[0][1] == True
        assert d[1][1] == True