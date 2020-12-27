from models import *  # set ONNX_EXPORT in models.py
from utils.datasets import *
from utils.utils import *
import os


class yolov3:
    def __init__(self, runpath='D:/Study/2020秋/软件工程/djangoProject/yolov3-archive'):
        print('----------init yolov3----------')
        os.chdir('D:/Study/2020秋/软件工程/djangoProject/yolov3-archive')
        self.cfg = 'cfg/yolov3-tiny.cfg'
        self.weights = 'weights/best.pt'
        self.source = '0'
        self.out = 'output_dir'
        self.imgsz = 512
        self.view_img = True

        # Initialize
        self.device = torch_utils.select_device(device='')
        if os.path.exists(self.out):
            shutil.rmtree(self.out)  # delete output folder
        os.makedirs(self.out)  # make new output folder

        # Initialize model
        self.model = Darknet(self.cfg, self.imgsz)

        # Load weights
        attempt_download(self.weights)
        self.model.load_state_dict(torch.load(self.weights, map_location=self.device)['model'])

        # Eval mode
        self.model.to(self.device).eval()

        # Fuse Conv2d + BatchNorm2d layers
        # model.fuse()

        # Get names and colors
        self.names = load_classes('data/coco.names')
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]

        self.img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # init img
        os.chdir(runpath)

    def detect_image(self, image):
        # Run inference
        t0 = time.time()
        img = self.img

        im0s = image
        # Padded resize
        img = letterbox(im0s, new_shape=self.imgsz)[0]
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = torch_utils.time_synchronized()
        pred = self.model(img, augment=False)[0]
        t2 = torch_utils.time_synchronized()

        # to float
        pred = pred.float()

        # Apply NMS
        pred = non_max_suppression(pred, 0.3, 0.6, multi_label=False, classes=None, agnostic=False)

        outimg = None
        # Process detections
        det = pred[0]
        s, im0 = '', im0s
        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  #  normalization gain whwh
        if det is not None and len(det):
            # Rescale boxes from imgsz to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += '%g %ss, ' % (n, self.names[int(c)])  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                label = '%s %.2f' % (self.names[int(cls)], conf)
                plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)])

        outimg = im0
        # Print time (inference + NMS)
        print('%sDone. (%.3fs)' % (s, t2 - t1))
        print('Done. (%.3fs)' % (time.time() - t0))
        return outimg
