from pico2d import load_image, get_time
from state_machine import StateMachine, time_out, space_down, right_down, left_up, left_down, right_up, start_event


# 상태를 클래스를 통해서 정의함
class Idle:

    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        boy.dir = 0
        boy.frame = 0
        # 현재 시간을 저장
        boy.start_time = get_time()

        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1: # 오른쪽을 바라보는 상태에서 눕기
            boy.image.clip_composite_draw(
                boy.frame*100, 300, 100, 100,
                3.141592/2, # 90도 회전 시계방향
                '', # 좌우상하 반전 x(H = 좌우반전, V = 상하반전)
                boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2,  # 90도 회전 시계방향
                '',  # 좌우상하 반전 x(H = 좌우반전, V = 상하반전)
                boy.x + 25, boy.y - 25, 100, 100
            )
        pass


class Run:
    @staticmethod
    def enter(boy, e):
    #     boy.dir = 1 # 오른쪽 방향
    #     boy.action = 1
    #     boy.frame = 0 # 세가지 변수가 실행되려면 enter함수가 실행되는게 선행되어야 함
        if right_down(e) or left_up(e): # 오른쪽으로 Run
            boy.dir = 1 # 오른쪽 방향
            boy.action = 1
        elif left_down(e) or right_up(e): # 왼쪽으로 Run
            boy.dir = -1
            boy.action = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action*100, 100, 100,
            boy.x, boy.y
        )
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 sate machine 생성
        self.state_machine.start(Idle) # 초기 상태가 Idle로 설정이 됨
        self.state_machine.set_transitions(
            {
                # Run : {}, # {} 내 생략 = Run 상태에서 어떤 이벤트가 들어와도 처리하지 않겠다.
                Idle : { right_down : Run, left_down : Run, left_up : Run, right_up : Run, time_out : Sleep },
                Run : { right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle},
                Sleep : { right_down : Run, left_down : Run, right_up : Run, left_up : Run, space_down : Idle }
            }
        )

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        # event : 입력 이벤트 key , mouse 등
        # 우리가 state machine에게 전달해줄 껀 튜플 ( , ) -> 가공
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()
        # self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
