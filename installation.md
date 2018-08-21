#Installer 만들기

해당 프로그램은 인스톨러를 만들기가 거지같이 어려웠다. 

본인의 개발환경은 python3.6 x86이며 PyQt5를 이용하였다. 
python은 2와 3에 걸쳐 있어 상당히 많은 이슈들을 내고 있다.
본인은 python2가 버려질 거라는 생각에 3를 고집해서 공부하고 있는데 가끔 한계에 봉착할 떄가 있다.
특히 deeplearning 부분은 많은 라이브러리가 2로 만들어져서 3와 호환이 안 좋다. 거의 호환된다고 할지라도 x64 버전에는 잘 먹지 않는다. 
그래서 어쩔 수 없이 x86을 쓰고 있다. 

근데 x86의 경우 pyinstaller로 exe 파일을 만들 때 에러가 무수히 뜨게 된다. 프로그램은 쉬운 거지만 exe 파일 만드는게 어렵다..
기억해두고자 여기 적어둔다.

1. 일단 PyQt5를 이용하면 PyQt5 라이브러리리를 캐야 한다.
 - ```%PYTHON_PATH%\Lib\site-packages\PyQt5\Qt\bin ```에 있는 ```*.dll```을 모두 모은다.
 - ```C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\Remote Debugger\x64```에서 ```api-ms-win-core-*.dll```을 모두 모은다.
 - 비주얼 스튜디오가 없다면 ```C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64```에서 ```api-ms-win-core-*.dll```을 모두 모으면 된다.
 - 이렇게 PyQt5와 Visual Studio에서 모은 dll들을 모두 모아 폴더(\dll)에 넣은 다음 패스에 같이 넣어 주어야 한다. 아래와 같이 ```-p \dlls```하면 된다.
 - 귀찮으면 본인이 같이 올려둔 ```\dll``` 폴더를 그대로 이용해도 된다. 

```pyinstaller --onefile --windowed --clean -p \dlls pygraph.py```

요거는 hidden import가 있는 경우에 사용한다. 
```pyinstaller --onefile --clean --hidden-import=tkinter --hidden-import=scipy --hidden-import=matplotlib -p \dlls pygraph.py```

2. 근데도 에러가 났다. wordcloud의 STOPWORDS 파일 때문인데 컴파일 후 임시 저장소에는 python파일이 아니면 가지 못하는데 이 때문에 같은 폴더 안에 있는 파일을 참조하는 코드가 에러가 난다. 이 경우, STOPWORDS 파일을 프로그램 내 바로 사용 가능한 형식으로 프린트하여 얻은 다음 프로그램 내부에 그냥 삽입해 버렸다. 참고로 라이브러리를 직접 손대야 하므로 주의를 요구한다.

3. 대충 이정도 삽질을 하면 양심껏 .exe 파일을 얻을 수 있다. 이틀 동안 머리 아프게 한 실행파일 만들기 안녕~~~ 잊어버리지 않겠다.ㅠㅠ