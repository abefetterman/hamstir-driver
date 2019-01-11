import argparse

from picamera import PiCamera

from PIL import Image

from aiy.vision.inference import CameraInference, ModelDescriptor, ImageInference
from aiy.vision.models import utils

def tensors_info(tensors):
    print([tensor.data for _,tensor in tensors.items()])
    return ', '.join('%s [%d elements]' % (name, len(tensor.data))
        for name, tensor in tensors.items())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', default='test_model', help='Model identifier.')
    parser.add_argument('--model_path', required=True, help='Path to model file.')
    parser.add_argument('--test_file', default=None, help='Path to test file.')
    args = parser.parse_args()

    model = ModelDescriptor(
        name=args.model_name,
        input_shape=(1, 192, 192, 3),
        input_normalizer=(0, 1),
        compute_graph=utils.load_compute_graph(args.model_path))
        
    if args.test_file:
        with ImageInference(model) as inference:
            image = Image.open(args.test_file)
            for result in inference.run(image):
                print('#%05d (%5.2f fps): %s' %
                    (inference.count, inference.rate, tensors_info(result.tensors)))

    with PiCamera(sensor_mode=4, framerate=30):
        with CameraInference(model) as inference:
            for result in inference.run():
                print('#%05d (%5.2f fps): %s' %
                    (inference.count, inference.rate, tensors_info(result.tensors)))


if __name__ == '__main__':
    main()