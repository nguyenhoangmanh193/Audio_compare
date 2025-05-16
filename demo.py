import mongoengine as me
import pandas as pd

# Kết nối MongoDB
me.connect('audio', host='mongodb+srv://onmontoan:biahoibuncha8862@cluster0.mhbsw.mongodb.net/audio?retryWrites=true&w=majority')

# Định nghĩa schema
class AudioFeature(me.Document):
    file_name = me.StringField()
    mfccs = me.StringField()
    energy = me.StringField()
    formant = me.StringField()
    spec = me.StringField()
    bandw = me.StringField()
    roof = me.StringField()
    meta = {'collection': 'audio_data'}

# Lấy dữ liệu từ MongoDB
docs = AudioFeature.objects()  # Lấy tất cả document

# Chuyển đổi thành list dict
data = []
for doc in docs:
    data.append({
        "file_name": doc.file_name,
        "mfccs": doc.mfccs,
        "energy": doc.energy,
        "formant": doc.formant,
        "spec": doc.spec,
        "bandw": doc.bandw,
        "roof": doc.roof
    })

# Tạo DataFrame
df = pd.DataFrame(data)
df.to_csv("Data/audio_data.csv", index=False)
print(df.head())  # In ra 5 dòng đầu tiên
