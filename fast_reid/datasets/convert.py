import os 
import json
import shutil
import pandas as pd
from collections import defaultdict

frame_path = '/home/zhaojin/datasets/REID_DATA/frames'
annotation_path = '/home/zhaojin/datasets/REID_DATA/annotations'
output_path = '/home/zhaojin/datasets/REID_DATA/dataset_frame_sort'
def sanity_check(annot):
    result = True
    message = ''
    ids = [False, False, False, False]
    for item in annot['shapes']:
        # print('item: ', item['label'], item['points'], item['shape_type'])
        if item['label'] not in ['1', '2', '3', '4', '11', '22', '33', '44']:
            result = False
            message += 'invalid class id: {}\n'.format(item['label'])
            break
        class_id = int(item['label'])
        
        if class_id in [1, 2, 3, 4]:
            ids[class_id-1] = True
            shape = item['shape_type']
            if shape == 'rectangle':
                x_min, y_min = item['points'][0]
                x_max, y_max = item['points'][1]
                # assert(x_min < x_max), 'x_min: {}, x_max: {}'.format(x_min, x_max)
                # assert(y_min < y_max), 'y_min: {}, y_max: {}'.format(y_min, y_max)
                if x_min < x_max and y_min < y_max:
                    pass
                else:
                    result = False
                    message += 'x_min: {}, x_max: {}, y_min: {}, y_max: {}\n'.format(x_min, x_max, y_min, y_max)
                    break
                    # print('x_min: {}, x_max: {}, y_min: {}, y_max: {}'.format(x_min, x_max, y_min, y_max))
                # print('x_min: ', x_min, 'y_min: ', y_min, 'x_max: ', x_max, 'y_max: ', y_max)
            # elif shape == 'point':
            #     gaze_x, gaze_y = item['points'][0]
            #     anno_dicts[class_id-1]['gaze'] = [int(gaze_x), int(gaze_y)]
                # print('gaze_x: ', gaze_x, 'gaze_y: ', gaze_y)
        else:
            pass
    for i in range(4):
        if not ids[i]:
            result = False
            message += 'class {} not found\n'.format(i+1)
    return result, message
for dir in os.listdir(annotation_path):
    if os.path.isdir(os.path.join(annotation_path, dir)):
        print('video name: ', dir)
        # os.makedirs(os.path.join(output_path, 'images', dir), exist_ok=True)
        # os.makedirs(os.path.join(output_path, 'annotations', dir), exist_ok=True)
        os.makedirs(os.path.join(output_path, dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_path, dir, 'gt'), exist_ok=True)
        os.makedirs(os.path.join(output_path, dir, 'dev'), exist_ok=True)
        annos = []
        devs = []
        processed_frame_name = 1
        for file in sorted(os.listdir(os.path.join(annotation_path, dir))):
            if file.endswith('.json'):
                anno = json.load(open(os.path.join(annotation_path, dir, file)))
                frame_name = file.split('.')[0] + '.jpg'
                # sanity_check_passed, sanity_message = sanity_check(anno)
                # if not sanity_check_passed:
                #     print('sanity check failed for frame {}: {}'.format(dir+'/'+frame_name, sanity_message))
                #     continue
                int_frame_name = str(int(frame_name[-7:-4]))
                has_body = False
                H = anno["imageHeight"]
                W = anno["imageWidth"]
                for item in anno['shapes']:
                    # print('item: ', item['label'], item['points'], item['shape_type'])
                    class_id = int(item['label'])
                    if class_id in [11, 22, 33, 44]:
                        has_body = True
                        break
                # print('frame name: ', frame_name)
                # print('frame name: ', frame_name)
                # print('keys: ', anno.keys()) # dict_keys(['version', 'flags', 'shapes', 'imagePath', 'imageData', 'imageHeight', 'imageWidth'])
                # anno_dicts = {
                #         'frame_name': frame_name,
                #         'class_id': i,
                #         'bbox': None,
                #         # 'gaze': [-1, -1],
                #     } 
                
                # print('anno_dicts: ', anno_dicts)
                for item in anno['shapes']:
                    # print('item: ', item['label'], item['points'], item['shape_type'])
                    class_id = int(item['label'])
                    if class_id in [11, 22, 33, 44]:
                        shape = item['shape_type']
                        if shape == 'rectangle':
                            x_min, y_min = item['points'][0]
                            x_max, y_max = item['points'][1]
                            # assert(x_min < x_max), 'x_min: {}, x_max: {}'.format(x_min, x_max)
                            # assert(y_min < y_max), 'y_min: {}, y_max: {}'.format(y_min, y_max)
                            # if x_min < x_max and y_min < y_max:
                            #     anno_dicts[(class_id//11)-1]['bbox'] = [int(x_min), int(y_min), int(x_max), int(y_max)]
                            if x_min > x_max:
                                x_min, x_max = x_max, x_min
                            if y_min > y_max:
                                y_min, y_max = y_max, y_min
                            # anno_dicts[frame_name] = {'frame_name': frame_name, 'id': (class_id//11)-1, 'bbox': [int(x_min), int(y_min), int(x_max), int(y_max)]}
                            results = [processed_frame_name, (class_id//11)-1, float(x_min), float(y_min), float(x_max)-float(x_min), float(y_max)-float(y_min), 1, -1, -1, -1]
                            results = [str(item) for item in results]
                            annos.append(','.join(results))
                            dev = [processed_frame_name, -1, float(x_min), float(y_min), float(x_max)-float(x_min), float(y_max)-float(y_min), 1, -1, -1, -1]
                            dev = [str(item) for item in dev]
                            devs.append(','.join(dev))
                            assert(x_min < x_max), 'x_min: {}, x_max: {}'.format(x_min, x_max)
                            assert(y_min < y_max), 'y_min: {}, y_max: {}'.format(y_min, y_max)
                            # print('x_min: {}, x_max: {}, y_min: {}, y_max: {}'.format(x_min, x_max, y_min, y_max))
                            # print('x_min: ', x_min, 'y_min: ', y_min, 'x_max: ', x_max, 'y_max: ', y_max)
                    else:
                        pass
                if has_body:
                    shutil.copy(os.path.join(frame_path, dir, frame_name), os.path.join(output_path, dir, 'images', (str(processed_frame_name)).zfill(7)+'.jpg'))
                    processed_frame_name += 1
        # with open(os.path.join(output_path, 'annotations', dir, 'gt.txt'), 'w') as f:
        with open(os.path.join(output_path, dir, 'gt', 'gt.txt'), 'w') as f:
            for item in annos:
                f.write(item + '\n')   
        with open(os.path.join(output_path, dir, 'dev', 'dev.txt'), 'w') as f:
            for item in devs:
                f.write(item + '\n')  

        #write seq file
        with open(os.path.join(output_path, dir, 'seqinfo.ini'), 'w') as f:
            f.write('[Sequence]\n')
            f.write('name={}\n'.format(dir))
            f.write('imDir=images\n')
            f.write('frameRate=5\n')
            f.write('seqLength={}\n'.format(processed_frame_name-1))
            f.write('imWidth={}\n'.format(W))
            f.write('imHeight={}\n'.format(H))
            f.write('imExt=.jpg\n')

        # break          
            
    else:
        print('here', dir)
        continue
