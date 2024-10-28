from pico2d import load_image, get_time
from state_machine import StateMachine, time_out, space_down


# 상태를 클래스를 통해서 정의함
class Idle:

    @staticmethod
    def enter(boy):
        # 현재 시간을 저장
        boy.start_time = get_time()

        pass

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy):
        pass

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(
            boy.frame*100, 300, 100, 100,
            3.141592/2, # 90도 회전 시계방향
            '', # 좌우상하 반전 x(H = 좌우반전, V = 상하반전)
            boy.x - 25, boy.y - 25, 100, 100
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
        self.state_machine.start(Sleep) # 초기 상태가 Idle로 설정이 됨
        self.state_machine.set_transitions(
            {
                Idle : { time_out : Sleep },
                Sleep : { space_down : Idle }
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
