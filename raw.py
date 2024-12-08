import subprocess
import time
import sys
import re

continuar = "y"
while continuar == "y":
    # Url pra fazer o download:
    URL = input('Type the .m3u8 link format: ')
    t1 = "Analyzing link..."
    n1 = 0
    for caractere in "Analyzing link...":
        print(t1[n1], end="", flush=True)
        n1 = n1+1
        time.sleep(0.05)
    time.sleep(1.34)
    print("\033[32m10%...20%...30%...40%...50%...60%...70%...80%...90%...Done\033[0m")
    time.sleep(0.5)
    print("\n")

    # Pasta do local do download e achar o path da pasta:
    pasta = input("\033[32mWhat will be the name of the folder where the file will be stored? (Please enter the name identical to the folder):\n\033[0m ")
    print("\033[1mFinding path...\033[0m")
    comandblock = ["find", "/", "-type", "d", "-name", pasta]
    execmdblck = subprocess.Popen(comandblock, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) 
    output, _ = execmdblck.communicate()
    path = output.decode().strip()
    


    comandblock1 = ['ls', '-l', path]
    execmdblck1 = subprocess.Popen(comandblock1, stdout=subprocess.PIPE)
    saida, _ = execmdblck1.communicate()
    # Contando o número de arquivos
    num_linhas = len(saida.decode().splitlines())

    Nome = input("What will be the name of the .mp4 file?\033[0m ")
    Nome = Nome + ".mp4"
    time.sleep(0.5)

    print("\n")
    print("\033[35mPlease confirm the file data:")
    print(f"URL: {URL})")
    print(f"Path: {path}")
    print(f"File name: {Nome}\033[0m")
    confirmacao = input("\033[1mIs the data correct?Y/N\n")
    if confirmacao == "Y" or confirmacao == "y":
        print("Saving file...")
    elif confirmacao == "N" or confirmacao == "n":
        print("Please restart the program...")
        sys.exit(1)

    # Comando para download com progresso
    comandblock2 = ["ffmpeg", "-i", URL, "-c", "copy", Nome, "-progress", "pipe:1"]

    try:
        process = subprocess.Popen(comandblock2, cwd=path, stderr=subprocess.PIPE, text=True)

        # Regex para pegar o tempo
        pattern = re.compile(r"time=(\d+:\d+:\d+\.\d+)")

        # Obtendo o tempo total do vídeo
        result = subprocess.run(["ffprobe", "-i", URL, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"], capture_output=True, text=True)
        duration = float(result.stdout.strip())
        # Monitorando o progresso
        for line in process.stderr:
            match = pattern.search(line)
            if match:
                time_str = match.group(1)
                hours, minutes, seconds = map(float, time_str.split(":"))
                current_time = hours * 3600 + minutes * 60 + seconds
                progress = (current_time / duration) * 100
                print(f"\rProgress: {progress:.2f}%", end="", flush=True)
        process.wait()
        print("\nDownload completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")

    continuacao = input("Do you want to restart program? Y/N ")
    if continuacao == "y" or continuacao == "Y":
        continuar = "y"
    else: 
        break
