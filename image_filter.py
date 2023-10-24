import os
import json
from PIL import Image

image_files_path = './원천데이터'
label_files_path = './라벨링데이터'
filter_lo_value = (0, 80, 180, 260)
target_size=(550, 550)

# JSON 파일 읽기
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data
        
# 카메라 각도 읽기
def camera_lo_value(data):
    return data["images"][0]["camera_lo"]

# 일반 or 전문의약품 정보 읽기
def drug_category(data):
    return data["images"][0]["di_etc_otc_code"]

# 이미지 크롭
def center_crop_images(path, target_size):
    if os.path.isfile(path):
        # 이미지를 OpenCV를 사용하여 읽어옴
        image = Image.open(path)
        if image is not None:
            # 이미지의 높이와 너비를 가져옴
            width, height = image.size

            # 가운데를 기준으로 자르기
            top = (height - target_size[0]) // 2
            bottom = top + target_size[0]
            left = (width - target_size[1]) // 2
            right = left + target_size[1]

            # 이미지를 가운데 크롭하고 저장
            cropped_image = image.crop((left, top, right, bottom))
            
            # 크롭한 이미지를 원래 파일 경로에 저장
            cropped_image.save(path)
            # print(f"{path}를 크롭했습니다.")
        else:
            print(f"Failed to read image: {path}")
    else:
        print(f'{path}가 없습니다.')


print('옳지않은 각도, 전문의약품 삭제중.....')
# 현재 디렉토리와 그 하위 디렉토리에서 JSON 파일 찾기
for root, dirs, files in os.walk(label_files_path):
    for file in files:
        if file.endswith(".json"):
            json_file_path = os.path.join(root, file)
            data = process_json_file(json_file_path)
            
            lo_value = camera_lo_value(data)
            drug = drug_category(data)
            
            if int(lo_value) not in filter_lo_value or drug != '일반의약품':
                # if int(lo_value) not in filter_lo_value:
                #     print(f'{json_file_path} : 올바른 각도가 아닙니다.')
                # if drug != '일반의약품':
                #     print(f'{json_file_path} : 일반의약품이 아닙니다.')
                    
                # JSON 파일과 동일한 이름의 PNG 파일 경로 구하기
                image_file_name = file.replace('.json', '.png')
                image_file_path = os.path.join(image_files_path, image_file_name)
                try:
                # 해당 JSON 파일 삭제
                    os.remove(json_file_path)
                    #print(f'{file_path} 삭제되었습니다.')
                except:
                    #print(f'{file_path} 파일이 없습니다.')
                    pass
                
                try:
                    # 해당 PNG 파일 삭제
                    os.remove(image_file_path)
                    #print(f'{image_file_path} 삭제되었습니다.')
                except:
                    #print(f'{image_file_path} 파일이 없습니다.')
                    pass
            else:
                image_file_name = file.replace('.json', '.png')
                image_file_path = os.path.join(image_files_path, image_file_name)
                center_crop_images(image_file_path, target_size)
print('작업이 완료되었습니다.')
input()


