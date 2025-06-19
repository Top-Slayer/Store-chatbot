from openai import OpenAI
import os

API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def get_quiz_bot_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content


def main():
    messages = [
        {
            "role": "system", "content": """ທ່ານເປັນ quiz bot ທີ່ຕະຫລົກ.
            ປະຕິບັດຕາມກົດລະບຽບ:
            1. ເຮັດແບບຖາມໃນຫົວຂໍ້ຕ່າງໆ
            2. ຖ້າຜູ້ໃຊ້ຕອບຖືກ, ໃຫ້ຊົມເຊີຍພວກເຮົາ
            3. ຖ້າຜູ້ໃຊ້ຕອບບໍ່ຖືກຕ້ອງ, ໃຫ້ຄໍາແນະນໍາແກ່ພວກເຂົາ
            4. ເຮັດແບບສອບຖາມຄັ້ງລະ 1 ແບບເທົ່ານັ້ນ
            5. ຖ້າຜູ້ໃຊ້ຕອບຖືກ, ໃຫ້ສ້າງແບບສອບຖາມໃຫມ່"""
        }
    ]

    print("QuizBot: Hello! ")

    while True:
        user_input = input("\nUser: ").strip()

        if user_input.lower() == "quit":
            print("\nQuizBot: Thanks you! See you next time!")
            break

        messages.append({"role": "user", "content": user_input})

        print(messages)

        bot_response = get_quiz_bot_response(messages)
        print(f"\nQuizBot: {bot_response}")

        messages.append({"role": "assist", "content": bot_response})


if __name__ == "__main__":
    main()