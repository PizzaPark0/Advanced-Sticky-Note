# Advanced-Sticky-Note
Sticky Note now can show image on top layer.

Reference(Title Bar) : https://soma0sd.tistory.com/96
_
1. 사용 전
- pyw파일을 그대로 사용하실 경우 pip install pyside2 필수
- python환경 없이 사용하실 경우, 프로젝트에 첨부해놓은 exe파일 받아서
  Stick Note.pyw 있는 위치에 붙여넣으시면 바로 사용할 수 있습니다. (https://github.com/PizzaPark0/Advanced-Sticky-Note/releases/tag/Memo)

_
2. 시용방법
- 프로그램을 실행하면 버튼 두개가 뜹니다. I는 이미지 박스 띄우는 버튼이고,
  T는 메모장 띄우는 버튼입니다. 각 상자는 아래에 설명하겠습니다.
- 이 프로그램은 종료할 때 현재 열려있는 상태의 메모장들을 모두 저장하고 창을 닫습니다.
  다시 실행할때 가장 마지막에 저장되어 있던 메모장들을 다시 열어줍니다.
- 저장하기 전에 그 전에 저장되어 있던건 다 삭제합니다. 중요한 내용은 닫아서 날리지 않도록 주의하세요.

_
3. 이미지 박스 : 말 그대로 이미지를 표시하는 메모장입니다.
- 로컬 파일을 드래그&드롭하거나, 클립보드의 이미지를 ctrl+v로 붙여넣어서 이미지를 표시할 수 있습니다.
- 창의 크기를 조정할 때, 이미지의 위치와 크기는 영향을 받지 않습니다. 대신 수동으로 이동할 수 있게 만들었습니다.
- 제목 표시줄은 통상적으로 표시하지 않고, 마우스를 갖다대면 표시됩니다.
- 단축키
  | ctrl+v : 클립보드의 이미지를 붙여넣습니다. 이미지가 아닌 경우 무시합니다.
  | ctrl+e : 이미지의 크기를 줄입니다.
  | ctrl+r : 이미지의 크기를 키웁니다.
  | 방향키 : 이미지를 창 안에서 이동시킵니다.
  | ctrl+tab : 항상 맨 앞에 놓일지에 대한 속성을 변환합니다.

_
3. 텍스트 박스 : 말 그대로 텍스트를 표시하는 메모장입니다.
- 전적으로 스티키 노트와 동일합니다. 다만 서식 변경은 안됩니다.
- 창의 크기를 조절하면 텍스트 박스의 크기도 함께 변합니다. 너무 작아지면 스크롤바가 생깁니다.
- 제목 표시줄은 통상적으로 표시하지 않고, 마우스를 갖다대면 표시됩니다.
- 단축키
  | ctrl+v : 클립보드의 이미지를 붙여넣습니다. 이미지가 아닌 경우 무시합니다.
  | ctrl+e : 글자 크기를 줄입니다.
  | ctrl+r : 글자 크기를 키웁니다.
  | ctrl+tab : 항상 맨 앞에 놓일지에 대한 속성을 변환합니다.
