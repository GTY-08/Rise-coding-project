import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# --- 1. 엑셀 파일 읽기 ---
file_path = "학원정보_재분류.xlsx"  # 실제 파일명으로 수정
df = pd.read_excel(file_path)

# --- 2. 사용자 입력 (Discrete 옵션) ---
print("수강 인원 선택:")
print("  1: 10인 미만")
print("  2: 10인 이상")
enrollment_choice = input("번호를 입력하세요: ").strip()
if enrollment_choice == "1":
    enrollment_filter = "10인 미만"
elif enrollment_choice == "2":
    enrollment_filter = "10인 이상"
else:
    print("잘못된 입력입니다. 기본값 '10인 미만'으로 설정합니다.")
    enrollment_filter = "10인 미만"

print("\n수강 연령층 선택:")
print("  1: 초등학생")
print("  2: 중학생")
print("  3: 고등학생")
age_choice = input("번호를 입력하세요: ").strip()
if age_choice == "1":
    age_filter = "초등학생"
elif age_choice == "2":
    age_filter = "중학생"
elif age_choice == "3":
    age_filter = "고등학생"
else:
    print("잘못된 입력입니다. 기본값 '초등학생'으로 설정합니다.")
    age_filter = "초등학생"

print("\n수강 과목 선택:")
print("  1: 국어")
print("  2: 수학")
print("  3: 영어")
print("  4: 과학")
subject_choice = input("번호를 입력하세요: ").strip()
if subject_choice == "1":
    subject_filter = "국어"
elif subject_choice == "2":
    subject_filter = "수학"
elif subject_choice == "3":
    subject_filter = "영어"
elif subject_choice == "4":
    subject_filter = "과학"
else:
    print("잘못된 입력입니다. 기본값 '국어'로 설정합니다.")
    subject_filter = "국어"

print("\n수강 목적 선택:")
print("  1: 내신")
print("  2: 수능 대비")
print("  3: 선행")
purpose_choice = input("번호를 입력하세요: ").strip()
if purpose_choice == "1":
    purpose_filter = "내신"
elif purpose_choice == "2":
    purpose_filter = "수능 대비"
elif purpose_choice == "3":
    purpose_filter = "선행"
else:
    print("잘못된 입력입니다. 기본값 '내신'으로 설정합니다.")
    purpose_filter = "내신"

# --- 3. 전체 데이터를 사용 (Discrete 점수 계산) ---
def condition_score(value, filter_str):
    return 1.0 if filter_str.lower() in str(value).lower() else 0.0

df["score_enrollment"] = df["수강 인원"].apply(lambda x: condition_score(x, enrollment_filter))
df["score_age"] = df["수강 연령층"].apply(lambda x: condition_score(x, age_filter))
df["score_purpose"] = df["수강 목적"].apply(lambda x: condition_score(x, purpose_filter))

# --- 4. 과목 전문성 가중치 ---
def subject_specialization_weight(subject_str, desired_subject):
    subjects = [s.strip() for s in str(subject_str).split(",")]
    if desired_subject in subjects:
        return 1.0 if len(subjects) == 1 else 0.4
    else:
        return 0.0

df["score_subject"] = df["수강 과목"].apply(lambda x: subject_specialization_weight(x, subject_filter))
# 희망 과목이 포함되지 않은 학원은 제외
df = df[df["score_subject"] > 0.0].copy()
if df.empty:
    print("\n희망 과목이 포함된 학원이 없습니다.")
    exit()

# --- 5. 텍스트 결합 ---
df["combined_text"] = (
    df["수강 과목"].astype(str) + " " +
    df["수강 목적"].astype(str) + " " +
    df["시설 및 편의 사항"].astype(str)
)

# --- 6. TextVectorization (TF-IDF) ---
max_tokens = 1000
vectorizer = layers.TextVectorization(max_tokens=max_tokens, output_mode="tf-idf")
vectorizer.adapt(df["combined_text"].values)
academy_vectors = vectorizer(df["combined_text"].values)

# --- 7. 신경망 모델 (임베딩 생성) ---
input_dim = academy_vectors.shape[1]
latent_dim = 16
embedding_model = keras.Sequential([
    keras.Input(shape=(input_dim,)),
    layers.Dense(64, activation="relu"),
    layers.Dense(latent_dim)
])
academy_latent = embedding_model(academy_vectors).numpy()

# --- 8. 추가 사용자 입력 (자유 텍스트) ---
user_free_text = input("\n추가적으로 원하는 학원 특성을 간단히 입력하세요 (예: '수능 대비 수학 선행'): ").strip()
if not user_free_text:
    user_free_text = subject_filter + " " + purpose_filter
user_vector = vectorizer([user_free_text])
user_latent = embedding_model(user_vector).numpy()

# --- 9. 코사인 유사도 계산 ---
def cosine_similarity(a, b):
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return np.dot(a_norm, b_norm.T)

text_similarities = cosine_similarity(academy_latent, user_latent).flatten()
# 과목 전문성 가중치(score_subject) 반영
effective_text_score = text_similarities * df["score_subject"]

# --- 10. 수치 정보 (평점, 추천율) ---
def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0

df["평점_norm"] = df["평점"].apply(lambda x: safe_float(x) / 5.0)
def normalize_recommend(x):
    val = safe_float(x)
    return val / 100.0 if val > 1 else val
df["추천율_norm"] = df["추천율"].apply(normalize_recommend)

numeric_score = (df["평점_norm"] * 0.3 + df["추천율_norm"] * 0.1)  # 총 0.4의 가중치

# --- 11. Discrete score 계산 ---
# 수강 인원: 0.5, 수강 연령층: 2.5, 수강 목적: 1.5 (총 4.5)
discrete_score = (df["score_enrollment"] * 0.5 +
                  df["score_age"] * 3 +
                  df["score_purpose"] * 1.5) / 5

# --- 12. 거리 점수 계산 ---
# 사용자 현재 위치 입력 및 지오코딩
geolocator = Nominatim(user_agent="academy_recommender")
user_address = input("\n현재 위치(주소)를 입력하세요: ").strip()
user_location = geolocator.geocode(user_address)
if user_location is None:
    print("사용자 위치를 찾을 수 없습니다. 기본 위치(대구 수성구)를 사용합니다.")
    user_coords = (35.846, 128.625)  # 예시 좌표 (대구 수성구)
else:
    user_coords = (user_location.latitude, user_location.longitude)

print('잠시만 기다려 주십시오')

def get_distance_score(address):
    try:
        loc = geolocator.geocode(address)
        if loc is None:
            return float('inf'), 0.0
        academy_coords = (loc.latitude, loc.longitude)
        distance = geodesic(user_coords, academy_coords).km
        # 가까울수록 높은 점수 (예: scale=5km)
        score = math.exp(-distance / 5)
        return distance, score
    except Exception as e:
        return float('inf'), 0.0

distances = []
distance_scores = []
for addr in df["위치"]:
    d, s = get_distance_score(addr)
    distances.append(d)
    distance_scores.append(s)

df["distance_km"] = distances
df["distance_score"] = distance_scores

# --- 13. 최종 점수 계산 ---
# 가중치: 텍스트 유사도 (w_text), 수치 정보 (w_numeric), discrete score (w_discrete), 거리 (w_distance)
w_text = 0.75
w_numeric = 0.3
w_discrete = 0.65
w_distance = 0.3

final_score = (w_text * effective_text_score +
               w_numeric * numeric_score +
               w_discrete * discrete_score +
               w_distance * df["distance_score"])
df["최종점수"] = final_score

# --- 14. 모든 학원 추천 결과 정렬 및 출력 ---
recommended_df = df.sort_values(by="최종점수", ascending=False)
print("\n추천 학원 순위:")
print(recommended_df[["학원이름", "수강 인원", "수강 연령층", "수강 과목", "수강 목적", "평점", "추천율", "distance_km", "최종점수"]].to_string(index=False))
