import asyncio, base64
from rodiumai import RodiumAI

async def main():
    client = RodiumAI()  # lit RODIUMAI_API_KEY depuis .env
    etape = "chat"
    while True:
        if etape == "chat":
            q = input("Votre question : ")
            r = await client.chat([{"role": "user", "content": q}])
            print(r.choices[0].message.content)
            print("Coût :", r.cost_rodi, "RODI")
        elif etape == "image":
            desc = input("Décrivez l'image : ")
            img = await client.images(model="openai/gpt-image-1", prompt=desc)
            with open("image.png", "wb") as f:
                f.write(base64.b64decode(img.data[0].b64_json))
            print("Image enregistrée : image.png")
        else:
            desc = input("Décrivez la vidéo : ")
            vid = await client.videos(model="google/veo-3.1-generate-preview",
                                      prompt=desc, duration_seconds=4, timeout=600)
            data = vid.data[0]
            if getattr(data, "b64_json", None):
                with open("video.mp4", "wb") as f:
                    f.write(base64.b64decode(data.b64_json))
            else:
                import requests
                v = requests.get(data.url, timeout=150)
                with open("video.mp4", "wb") as f:
                    f.write(v.content)
            print("Vidéo enregistrée : video.mp4")
        suite = input("Revenir (b) / rester (r) / suivant (s) / quitter (q) ? ").strip().lower()
        ordre = ["chat", "image", "video"]
        i = ordre.index(etape)
        if suite == "b" and i > 0:
            etape = ordre[i-1]
        elif suite == "s" and i < 2:
            etape = ordre[i+1]
        elif suite == "q":
            break

asyncio.run(main())
