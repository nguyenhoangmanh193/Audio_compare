import json
import io
import mongoengine as me
import requests
from  dactrung import  mfcc, energy_contour, formant_f1_f2, spactral_centroid, bandwind, roof_off
import time
# Kết nối MongoDB với URI
me.connect(
    db="audio",
    host="mongodb+srv://onmontoan:biahoibuncha8862@cluster0.mhbsw.mongodb.net/audio?retryWrites=true&w=majority"
)

# Định nghĩa schema/model
class AudioFeature(me.Document):
    file_name = me.StringField(required=True, unique=True)     # Tên file audio
    mfccs = me.StringField()                        # Chuỗi dữ liệu mô tả hoặc JSON string (tùy bạn lưu gì)
    energy = me.StringField()
    formant = me.StringField()
    spec = me.StringField()
    bandw = me.StringField()
    roof = me.StringField()
    meta = {
        'collection': 'audio_data'  # Tên collection trong MongoDB
}
# Đọc lại từ file
with open("Data/my_list.json", "r") as f:
    loaded_list = json.load(f)


q=0
for i in range(13,14):
       try:
           dropbox_preview_link = loaded_list[i]

           # Chuyển link preview thành link tải file nhị phân trực tiếp
           direct_url = dropbox_preview_link.replace("dl=0", "dl=1")
           try:
               response = requests.get(direct_url)
           except Exception as e:
               print(e)
           if response.status_code != 200:
               print("Lỗi tải file:", response.status_code)
           audio_bytes = io.BytesIO(response.content)

           m = mfcc(audio_bytes)
           e = energy_contour(audio_bytes)
           formant = formant_f1_f2(audio_bytes)

           audio_bytes = io.BytesIO(response.content)

           s = spactral_centroid(audio_bytes)
           audio_bytes = io.BytesIO(response.content)
           band = bandwind(audio_bytes)
           audio_bytes = io.BytesIO(response.content)
           r = roof_off(audio_bytes)
           audio_bytes = io.BytesIO(response.content)

           feature = AudioFeature(file_name=dropbox_preview_link, mfccs=m, energy=e, formant=formant, spec=s,
                                  bandw=band, roof=r)
           feature.save()
           print("Đã lưu document với id:", feature.file_name)
           print(q)
           q+=1


       except Exception as e:
           print(e)
           continue

