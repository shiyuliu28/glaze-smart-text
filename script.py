from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)


def convert_to_elaborate_text(text):
    prompt = '''
    convert the following text to be more elaborate and detailed, especially for any jargons involved.
    input: "%s"
    output:
    ''' % (text)
    return prompt


def run_gpt_convert_to_elaborate_text(text, temperature=0.5, retry=3):
    # -----this uses gpt 3.5---------
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=convert_to_elaborate_text(text),
        max_tokens=1000,
        temperature=temperature
    )

    # -----this uses gpt 4---------
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "user", "content": get_gpt_size_prompt(size, category)},
    #     ],
    #     max_tokens=120,
    #     temperature=temperature
    # )

    return response.choices[0].text

def get_book_summaries_and_save(title, save_to_dir="result/", temperature=0.5):
    prompt = '''
    Give a comprehensive, 30-minute summary of "%s" in a chapter-by-chapter format.
    Output:
    ''' % title  # Use only one placeholder for the title


    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=4000,
        temperature=temperature
    )

    summary_text = response.choices[0].text.strip()

    os.makedirs(save_to_dir, exist_ok=True)

    file_path = os.path.join(save_to_dir, f"{title.replace(' ', '_')}_summary.txt")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print(f"Summary saved to {file_path}")

    return response.choices[0].text

    

if __name__ == "__main__":
#   text = '''
#     Volcanoes form when magma rises to the Earth's surface through vents and fissures. Magma is created when rocks melt deep within the Earth due to intense heat. The process of magma formation can occur in a few ways:
#     Subduction
#     When two tectonic plates move towards each other, the denser plate is forced beneath the other. This process is called subduction. As the plate sinks, it heats up and releases water from the minerals and sediments within it. The water lowers the melting point of the mantle, creating magma.
#     Hotspot volcanism
#     A hotspot is a zone of magmatic activity within a tectonic plate. The hotspot remains relatively stationary, while the tectonic plate moves slowly over it. This process can create a line of volcanoes or islands. The Hawaiian volcanic chain is thought to have formed in this way. 
#     Once magma reaches the surface, it erupts as lava. Volcanoes also release gases and ash. Over time, volcanoes grow larger and larger through repeated eruptions
#     '''
#   print(run_gpt_convert_to_elaborate_text(text))

    title = "Atomic Habit"
    get_book_summaries_and_save(title)