import asyncio, json, glob, os, sys
import edge_tts
VOICES=open("voix/voice.txt").read().split(); RATE=open("voix/rate.txt").read().strip()
async def one(v,f):
    n=os.path.basename(f)[:-4]; text=open(f,encoding="utf-8").read()
    c=edge_tts.Communicate(text,v,rate=RATE,boundary="WordBoundary")
    words=[]; audio=bytearray()
    async for ch in c.stream():
        if ch["type"]=="audio": audio+=ch["data"]
        elif ch["type"]=="WordBoundary": words.append({"t":ch["offset"]/1e7,"d":ch["duration"]/1e7,"w":ch["text"]})
    open(f"out/{v}_{n}.mp3","wb").write(audio); json.dump(words,open(f"out/{v}_{n}.json","w"),ensure_ascii=False)
async def main():
    os.makedirs("out",exist_ok=True)
    for f in sorted(glob.glob("voix/textes/*.txt")):
        for v in VOICES: await one(v,f)
asyncio.run(main())
