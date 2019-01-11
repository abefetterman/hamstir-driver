import argparse
import time

from gpiozero import Motor
from picamera import PiCamera
from PIL import Image

from aiy.vision.inference import CameraInference, ModelDescriptor, ImageInference
from aiy.vision.models import utils
from aiy.pins import PIN_A,PIN_B,PIN_C,PIN_D

def tensors_info(tensors):
    print([tensor.data for _,tensor in tensors.items()])
    return ', '.join('%s [%d elements]' % (name, len(tensor.data))
        for name, tensor in tensors.items())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', default='test_model', help='Model identifier.')
    parser.add_argument('--model_path', required=True, help='Path to model file.')
    parser.add_argument('--speed', default=0.5, help='Reduction factor on speed')
    args = parser.parse_args()

    model = ModelDescriptor(
        name=args.model_name,
        input_shape=(1, 192, 192, 3),
        input_normalizer=(0, 1),
        compute_graph=utils.load_compute_graph(args.model_path))
        
    left = Motor(PIN_A, PIN_B)
    right = Motor(PIN_C, PIN_D)
    print('spinning')
    
    try:
        with PiCamera(sensor_mode=4, framerate=30):
            with CameraInference(model) as inference:
                for result in inference.run():
                    data = [tensor.data for _,tensor in result.tensors.items()]
                    lspeed,rspeed = data[0]
                    print('#%05d (%5.2f fps): %1.2f/%1.2f' %
                        (inference.count, inference.rate, lspeed, rspeed))
                    if lspeed < 0:
                        left.reverse(-max(-1,lspeed) * args.speed)
                    else:
                        left.forward(min(1,lspeed) * args.speed)
                    if rspeed < 0:
                        right.reverse(-max(-1,rspeed) * args.speed)
                    else:
                        right.forward(min(1,rspeed) * args.speed)
    
    except Exception as e: 
        left.stop()
        right.stop()
        print(e)


if __name__ == '__main__':
    main()