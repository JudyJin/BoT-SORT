import os 
import json
import shutil
import pandas as pd
frame_path = 'frames'
annotation_path = 'annotations'
output_path = 'dataset'
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
        os.makedirs(os.path.join(output_path, 'images', dir), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'annotations', dir), exist_ok=True)
        annos = [[], [], [], []]
        print(annos)
        for file in os.listdir(os.path.join(annotation_path, dir)):
            if file.endswith('.json'):
                anno = json.load(open(os.path.join(annotation_path, dir, file)))
                frame_name = file.split('.')[0] + '.jpg'
                sanity_check_passed, sanity_message = sanity_check(anno)
                if not sanity_check_passed:
                    print('sanity check failed for frame {}: {}'.format(dir+'/'+frame_name, sanity_message))
                    continue

                shutil.copy(os.path.join(frame_path, dir, frame_name), os.path.join(output_path, 'images', dir, frame_name))
                print('frame name: ', frame_name)
                # print('keys: ', anno.keys()) # dict_keys(['version', 'flags', 'shapes', 'imagePath', 'imageData', 'imageHeight', 'imageWidth'])
                anno_dicts = [{
                        'frame_name': frame_name,
                        'bbox': None,
                        'gaze': [-1, -1],
                    } for i in range(4)]
                # print('anno_dicts: ', anno_dicts)
                for item in anno['shapes']:
                    # print('item: ', item['label'], item['points'], item['shape_type'])
                    class_id = int(item['label'])
                    if class_id in [1, 2, 3, 4]:
                        shape = item['shape_type']
                        if shape == 'rectangle':
                            x_min, y_min = item['points'][0]
                            x_max, y_max = item['points'][1]
                            # assert(x_min < x_max), 'x_min: {}, x_max: {}'.format(x_min, x_max)
                            # assert(y_min < y_max), 'y_min: {}, y_max: {}'.format(y_min, y_max)
                            if x_min < x_max and y_min < y_max:
                                anno_dicts[class_id-1]['bbox'] = [int(x_min), int(y_min), int(x_max), int(y_max)]
                            else:
                                assert(x_min < x_max), 'x_min: {}, x_max: {}'.format(x_min, x_max)
                                assert(y_min < y_max), 'y_min: {}, y_max: {}'.format(y_min, y_max)
                                # print('x_min: {}, x_max: {}, y_min: {}, y_max: {}'.format(x_min, x_max, y_min, y_max))
                            # print('x_min: ', x_min, 'y_min: ', y_min, 'x_max: ', x_max, 'y_max: ', y_max)
                        elif shape == 'point':
                            gaze_x, gaze_y = item['points'][0]
                            anno_dicts[class_id-1]['gaze'] = [int(gaze_x), int(gaze_y)]
                            # print('gaze_x: ', gaze_x, 'gaze_y: ', gaze_y)
                    else:
                        pass
                for i in range(4):
                    if anno_dicts[i]['bbox'] is not None:
                        result = []
                        result.append(anno_dicts[i]['frame_name'])
                        for j in range(4):
                            result.append(str(anno_dicts[i]['bbox'][j]))
                        for j in range(2):
                            result.append(str(anno_dicts[i]['gaze'][j]))
                        annos[i].append(','.join(result))
            #             print(','.join(result))
            #             print('anno_dicts ', i+1, anno_dicts[i])
            #             print('annos ', i+1, annos[i])
            # # foo
            # for i in range(4):
            #     print('annos ', i+1, annos[i])
        for i in range(4):
            # print('annos ', i+1, annos[i])
            with open(os.path.join(output_path, 'annotations', dir, 's%2d.txt' % (i+1)), 'w') as f:
                for item in annos[i]:
                    f.write(item + '\n')                
            
    else:
        print('here', dir)
        continue
