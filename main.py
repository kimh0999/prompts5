"""프롬프트 관리 프로그램

자주 쓰는 생성형 AI 프롬프트를 메모리에 저장하고 조회하는 콘솔 프로그램입니다.
Python 3.10 이상에서 실행하세요.
"""

# 결과물의 형태가 아니라 '사용 목적'을 기준으로 나눈 분류입니다.
CATEGORIES = [
    "요약·분석",
    "개발·코딩",
    "기획·문서화",
    "콘텐츠 제작",
    "업무 자동화",
    "학습·교육",
    "취업·커리어",
    "기타",
]


def create_default_prompts():
    """프로그램 시작 시 기본으로 등록되는 프롬프트 목록을 만들어 돌려줍니다."""
    return [
        {
            "id": 1,
            "title": "IT 뉴스 요약 및 분류",
            "category": "요약·분석",
            "purpose": "IT 뉴스의 핵심 내용과 기술 동향 파악",
            "content": (
                "아래 IT 뉴스 기사를 읽고 다음 형식으로 정리해줘.\n"
                "1. 한 줄 요약\n"
                "2. 핵심 내용 3가지\n"
                "3. 관련 기술 분야 분류\n"
                "4. 개발자 입장에서 주목할 점\n\n"
                "기사: [기사 본문을 여기에 붙여넣기]"
            ),
            "tags": ["IT", "뉴스", "요약", "동향"],
            "model": "ChatGPT",
            "favorite": False,
        },
        {
            "id": 2,
            "title": "ReqMate 요구사항 문서화",
            "category": "기획·문서화",
            "purpose": "회의 내용을 정리된 요구사항 명세로 변환",
            "content": (
                "너는 요구사항 분석 전문가야.\n"
                "아래 회의 내용을 읽고 요구사항 명세서를 작성해줘.\n\n"
                "출력 형식:\n"
                "- 기능 요구사항 (ID, 설명, 우선순위)\n"
                "- 비기능 요구사항\n"
                "- 제약 조건\n"
                "- 확인이 필요한 모호한 부분\n\n"
                "회의 내용: [회의록을 여기에 붙여넣기]"
            ),
            "tags": ["요구사항", "문서화", "기획", "ReqMate"],
            "model": "Claude",
            "favorite": False,
        },
        {
            "id": 3,
            "title": "C 언어 코드 오류 분석",
            "category": "개발·코딩",
            "purpose": "C 코드의 컴파일 오류와 논리 오류 원인 파악",
            "content": (
                "아래 C 코드를 분석해줘.\n"
                "1. 컴파일 오류가 있다면 원인과 수정 방법\n"
                "2. 논리적 오류나 잠재적 버그\n"
                "3. 메모리 관련 문제 (누수, 범위 초과 등)\n"
                "4. 수정한 전체 코드\n\n"
                "초보자가 이해할 수 있게 왜 그런지 설명도 붙여줘.\n\n"
                "코드:\n[C 코드를 여기에 붙여넣기]"
            ),
            "tags": ["C", "디버깅", "코드리뷰", "오류"],
            "model": "Claude",
            "favorite": False,
        },
        {
            "id": 4,
            "title": "재고 부족 감지 자동화 설계",
            "category": "업무 자동화",
            "purpose": "재고 데이터를 점검해 부족 항목을 자동으로 알리는 절차 설계",
            "content": (
                "재고 관리 자동화 흐름을 설계해줘.\n\n"
                "조건:\n"
                "- 입력 데이터: 품목명, 현재 수량, 안전 재고 기준\n"
                "- 현재 수량이 안전 재고보다 적으면 부족으로 판단\n"
                "- 부족 항목을 목록으로 정리해 담당자에게 알림\n\n"
                "출력 형식:\n"
                "1. 처리 절차 단계별 설명\n"
                "2. 필요한 데이터 항목\n"
                "3. 예외 상황과 대응 방법"
            ),
            "tags": ["재고", "자동화", "업무", "알림"],
            "model": "ChatGPT",
            "favorite": False,
        },
    ]


def get_non_empty_input(message):
    """빈 값을 거부하고, 값이 들어올 때까지 다시 물어봅니다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("값을 입력해주세요.")


def get_multiline_input(message):
    """여러 줄을 입력받습니다. END만 적힌 줄이 나오면 입력이 끝난 것으로 봅니다.

    프롬프트 내용은 대부분 여러 줄이라 input() 한 번으로는 받을 수 없습니다.
    빈 줄을 종료 신호로 쓰지 않는 이유는, 프롬프트 안에서 문단을 나누는 데
    빈 줄을 쓰는 경우가 많아 내용이 중간에 잘리기 때문입니다.
    """
    while True:
        print(message)
        print("(입력을 마치려면 END만 적고 엔터를 누르세요)")

        lines = []
        while True:
            line = input("> ")
            if line.strip() == "END":
                break
            lines.append(line)

        # 앞뒤 빈 줄만 정리하고, 문단을 나누는 중간 빈 줄은 그대로 둡니다.
        content = "\n".join(lines).strip()
        if content:
            return content
        print("내용을 입력해주세요.")


def show_menu():
    """메인 메뉴를 출력합니다."""
    print()
    print("=" * 40)
    print(" 프롬프트 관리 프로그램")
    print("=" * 40)
    print(" 1. 프롬프트 추가")
    print(" 2. 전체 목록 보기")
    print(" 3. 카테고리별 조회")
    print(" 4. 키워드 검색")
    print(" 5. 프롬프트 상세 보기")
    print(" 6. 즐겨찾기 추가·해제")
    print(" 7. 즐겨찾기 목록 보기")
    print(" 0. 프로그램 종료")
    print("=" * 40)


def main():
    prompts = create_default_prompts()
    print(f"기본 프롬프트 {len(prompts)}개를 불러왔습니다.")

    while True:
        show_menu()
        choice = input("번호를 선택하세요: ").strip()

        match choice:
            case "0":
                print("프로그램을 종료합니다.")
                break
            case "1" | "2" | "3" | "4" | "5" | "6" | "7":
                print("아직 구현되지 않은 기능입니다.")
            case _:
                print("메뉴에 있는 번호(0~7)를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C를 누르거나 입력이 끊겼을 때 오류 화면 대신 조용히 끝냅니다.
        print()
        print("프로그램을 종료합니다.")
