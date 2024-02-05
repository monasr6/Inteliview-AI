import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity


def getAnswerSimilarity(model_ans,cand_ans,model):
    model_ans = """As a seasoned professional with a proven track record in project management, I bring a blend of leadership, creativity, and analytical skills. My ability to deliver results on time and within budget, coupled with my innovative problem-solving approach, positions me as an asset to your team. I am passionate about leveraging my expertise to drive efficiency, foster collaboration, and contribute to the growth of your organization. With a commitment to excellence, I am eager to bring my skills to the table and contribute to the success of your dynamic team."""
    cand_ans = """As someone who thrives in dynamic environments, my unconventional yet effective approach to project management sets me apart. With a background in creative problem-solving and adaptability, I bring a unique perspective to the table. My ability to think outside the box and embrace ambiguity allows me to navigate complex projects with enthusiasm. I am eager to contribute my innovative mindset to your team, fostering a culture of continuous improvement and driving successful outcomes. By leveraging my non-traditional approach, I believe I can bring fresh ideas and energy to elevate your project management initiatives."""
    docs = [(model_ans) , (cand_ans)]
    embeddings1 = model(docs)
    similarity1 = cosine_similarity(embeddings1)
    return similarity1[0][1]

def load_model():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    return model