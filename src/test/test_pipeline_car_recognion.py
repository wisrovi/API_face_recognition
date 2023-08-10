from main import car_recognition


class TestPipelineCarRecognion:
    def test_pipeline_car_recognion(self):
        data = { 
            "source": "/test/theft_vehicles/scene.png"    
        }
        result_car = car_recognition(data)
        assert len(result_car) == 3
        assert result_car[0]["name"] == "20 DYB!"