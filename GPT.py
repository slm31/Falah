import time
from openai import OpenAI

# إعداد مفتاح OpenAI API ومعرف المساعد
OPENAI_API_KEY = "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"  # استبدل بمفتاح OpenAI الخاص بك
ASSISTANT_ID = "asst_6oadhNqT43dLfCQVhOndBvnD"  # معرف المساعد الخاص بك

# إنشاء عميل OpenAI باستخدام المفتاح
client = OpenAI(api_key=OPENAI_API_KEY)

# دالة الدردشة مع ChatGPT للحصول على اللعبة
def suggest_game(players, ages, occasion, duration, interaction, participant_names):
    """
    إرسال البيانات إلى GPT API باستخدام Assistant ID لتحديد اللعبة المناسبة.
    
    Args:
        players (str): عدد اللاعبين.
        ages (str): أعمار اللاعبين.
        occasion (str): نوع المناسبة.
        duration (str): مدة اللعبة.
        interaction (str): نوع التفاعل المطلوب.
        participant_names (list): قائمة بأسماء المشاركين.
    
    Returns:
        str: اسم اللعبة المناسبة أو رسالة خطأ.
    """
    try:
        # إعداد البيانات التي سيتم إرسالها
        data = f"""
        عدد اللاعبين: {players}.
        أعمار اللاعبين: {ages}.
        نوع المناسبة: {occasion}.
        مدة اللعبة: {duration}.
        نوع التفاعل المطلوب: {interaction}.
        أسماء المشاركين: {', '.join(participant_names)}.
        """

        # إنشاء جلسة جديدة مع الرسائل
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": data  # البيانات الآن نص وليس كائن
                }
            ]
)

        # بدء تشغيل المساعد باستخدام Assistant ID
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
        print(f"👉 Run Created: {run.id}")

        # انتظار انتهاء العملية
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"🏃 Run Status: {run.status}")
            time.sleep(1)

        print(f"🏁 Run Completed!")

        # جلب الرد النهائي من ChatGPT
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        latest_message = messages[0]
        print(f"📝 Sending data to GPT: players={players}, ages={ages}, occasion={occasion}, duration={duration}, interaction={interaction}, names={participant_names}")

        # إعادة نص الرد النهائي
        return latest_message.content[0].text.value

    except Exception as e:
        print(f"❌ Error during ChatGPT API call: {e}")
        return "فشل في الحصول على اللعبة المناسبة."
