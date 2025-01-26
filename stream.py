import streamlit as st
from GPT import suggest_game  # استيراد دالة `suggest_game` من ملف GPT.py

# تحسين الواجهة العامة
st.set_page_config(page_title="فــلّــة - اختر لعبتك", page_icon="🎉", layout="centered")

# عنوان التطبيق مع زينة
st.markdown("<h1 style='text-align: center; color: #FF5733;'>🎲 فــلّــة 🎉</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>اختر لعبتك المثالية لجعل تجمعاتك أكثر متعة!</p>", unsafe_allow_html=True)

# إضافة فاصل زخرفي
st.markdown("---")

# الأسئلة
st.markdown("<h3 style='color: #4CAF50;'>📝 أجب عن الأسئلة التالية:</h3>", unsafe_allow_html=True)

# عدد اللاعبين باستخدام Slider
num_players = st.slider("كم عدد اللاعبين؟ 🎮", min_value=1, max_value=15, value=5)

# أعمار اللاعبين
ages = st.selectbox("🎂 ما الفئة العمرية للمشاركين؟", ["أقل من 10 سنوات", "10-15 سنة", "16-20 سنة", "21 سنة فأكثر"])

# أسماء اللاعبين (بناءً على عدد اللاعبين المحدد)
st.markdown("<h4 style='color: #FFC300;'>🧑‍🤝‍🧑 أسماء المشاركين:</h4>", unsafe_allow_html=True)
participant_names = []
for i in range(num_players):
    name = st.text_input(f"اسم اللاعب {i+1}:", key=f"name_{i+1}")
    if name:
        participant_names.append(name)

# نوع المناسبة
occasion = st.selectbox("🎉 نوع المناسبة:", ["تجمع عائلي", "حفلة أصدقاء", "نشاط مدرسي"])

# مدة اللعبة
duration = st.text_input("⏳ كم المدة المتاحة للعب؟ (مثلاً: 30 دقيقة)")

# نوع التفاعل المطلوب
interaction = st.radio("⚡ نوع التفاعل المطلوب:", ["حركة ونشاط بدني", "أسئلة وألغاز", "حديث اجتماعي"])

# إضافة فاصل زخرفي قبل زر الإرسال
st.markdown("---")

# زر الإرسال
if st.button("🎁 احصل على لعبتك"):
    # التحقق من المدخلات
    if not duration or len(participant_names) < num_players:
        st.warning("⚠️ يرجى تعبئة جميع الحقول وإضافة أسماء المشاركين!")
    else:
        # استدعاء دالة اقتراح اللعبة وتمرير جميع المدخلات
        game = suggest_game(num_players, ages, occasion, duration, interaction, participant_names)

        # عرض النتيجة
        if game:
            st.success(f"🎉 اللعبة المناسبة لك: {game}")
            st.markdown("<h4 style='color: #FFC300;'>**أسماء المشاركين:**</h4>", unsafe_allow_html=True)
            for name in participant_names:
                st.write(f"- {name}")

            # إعداد النص لحفظه في ملف
            game_details = f"""
            اللعبة المناسبة لك:
            {game}

            تفاصيل المدخلات:
            عدد اللاعبين: {num_players}
            أعمار المشاركين: {ages}
            نوع المناسبة: {occasion}
            مدة اللعبة: {duration}
            نوع التفاعل المطلوب: {interaction}

            أسماء المشاركين:
            {', '.join(participant_names)}
            """

            # زر لتحميل اللعبة كملف نصي
            st.download_button(
                label="📥 احفظ اللعبة",
                data=game_details,
                file_name="لعبتي.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ حدث خطأ أثناء الحصول على اللعبة المناسبة. يرجى المحاولة مرة أخرى.")

# إضافة فاصل زخرفي في النهاية
st.markdown("<hr style='border: 2px solid #FF5733;'>", unsafe_allow_html=True)


