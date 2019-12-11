from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_restart(self, event):
        text = event.message.text
        return text.lower() == "結束遊戲"

    def on_enter_start(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入 開始遊戲 以開始遊玩")

    def is_going_to_background(self, event):
        text = event.message.text
        return text.lower() == "開始遊戲"

    def is_going_to_description(self, event):
        text = event.message.text
        return text.lower() == "遊戲說明"

    def on_enter_background(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        f.write('16\n2000000\n40\n3000000\n25')
        f.close()
        send_text_message(reply_token, "2016年，蔡英文拿下了總統大選的勝利，成為了台灣史上第一位女總統。但為了競選連任，她還得更加努力才行。")

    def on_enter_description(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "遊戲目的：幫助蔡英文贏得2020總統大選\n
                                        遊玩方式：\n
                                        在面臨選擇時輸入是/否\n
                                        其餘時候輸入繼續")

    def is_going_to_16_18(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_16_18(self, event):
        reply_token = event.reply_token
        f = open("gamedata.txt", "r")
        send_text_message(reply_token, "西元：          20" + f.readline() +
                                       "綠營支持者：" + f.readline() +
                                       "綠營投票率：" + f.readline() +
                                       "藍營支持者：" + f.readline() +
                                       "藍營投票率：" + f.readline())
        f.close()

    def is_going_to_event_16_18(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = f.readline()
        y = year.split("\n")
        f.close()
        return (text.lower() == "繼續") and ((y[0] == "16") or (y[0] == "17"))

    def on_enter_event_16_18(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        if year == 16:
            send_text_message(reply_token, "朝野和全國上下正為了一例一休吵得不可開交，是否要繼續推動一例一休呢？")
        elif year == 17:
            send_text_message(reply_token, "反年改團體正走上街頭進行抗爭，")

    def is_going_to_kaohsiung(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and (year == 18)

    def on_enter_kaohsiung(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "高雄市長選舉")

    def is_going_to_fish_win(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_fish_win(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "韓國瑜勝選")

    def is_going_to_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "西元：      " + f.readline() +
                                       "綠營支持者：" + f.readline() +
                                       "綠營投票率：" + f.readline() +
                                       "藍營支持者：" + f.readline() +
                                       "藍營投票率：" + f.readline())
        f.close()

    def is_going_to_event_18_20_win(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and ((year == 18) or (year == 19))

    def on_enter_event_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        if year == 18:
            send_text_message(reply_token, "韓國瑜請假")
        elif year == 19:
            send_text_message(reply_token, "香港")

    def is_going_to_battle_win(self, event):
        text = event.message.text
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        return (text.lower() == "繼續") and (year == 20)

    def on_enter_battle_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "選舉開始")
        
    def is_going_to_fish_lose(self, event):
        text = event.message.text
        return text.lower() == "是"

    def on_enter_fish_lose(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "韓國瑜敗選")

    def is_going_to_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "西元：      " + f.readline() +
                                       "綠營支持者：" + f.readline() +
                                       "綠營投票率：" + f.readline() +
                                       "藍營支持者：" + f.readline() +
                                       "藍營投票率：" + f.readline())
        f.close()

    def is_going_to_event_18_20_lose(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and ((year == 18) or (year == 19))

    def on_enter_event_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        if year == 18:
            send_text_message(reply_token, "韓國瑜演講")
        elif year == 19:
            send_text_message(reply_token, "香港")

    def is_going_to_battle_lose(self, event):
        text = event.message.text
        f = open('gamedata', 'r')
        year = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and (year == 20)

    def on_enter_battle_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "選舉開始")

    def is_going_to_result_win(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(readline())
        green_people = int(readline())
        green_rate = int(readline())
        blue_people = int(readline())
        blue_rate = int(readline())
        f.close()
        return (text.lower() == "選舉結果") and ((green_people * green_rate)) > (blue_people * blue_rate)


    def on_enter_result_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "勝選")
        self.go_back()
        
    def is_going_to_result_lose(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(readline())
        green_people = int(readline())
        green_rate = int(readline())
        blue_people = int(readline())
        blue_rate = int(readline())
        f.close()
        return (text.lower() == "選舉結果") and ((green_people * green_rate)) < (blue_people * blue_rate)

    def on_enter_result_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "敗選")
        self.go_back()

    def is_going_to_yes_event_16_18(self, event):
        text = event.message.text
        return text.lower() == "是"

    def on_enter_yes_event_16_18(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 16:
            send_text_message(reply_token, "yes")
        elif year == 17:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_no_event_16_18(self, event):
        text = event.message.text
        return text.lower() == "否"

    
    def on_enter_no_event_16_18(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 16:
            send_text_message(reply_token, "yes")
        elif year == 17:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(year + "\n" + green_people + "\n" + green_rate + "\n" + blue_people + "\n" + blue_rate)
        f.close()

    def is_going_to_yes_event_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "是"
        
    def on_enter_yes_event_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            send_text_message(reply_token, "yes")
        elif year == 19:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(year + "\n" + green_people + "\n" + green_rate + "\n" + blue_people + "\n" + blue_rate)
        f.close()

    def is_going_to_no_event_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_no_event_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            send_text_message(reply_token, "yes")
        elif year == 19:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(year + "\n" + green_people + "\n" + green_rate + "\n" + blue_people + "\n" + blue_rate)
        f.close()

    def is_going_to_yes_event_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "是"

    def on_enter_yes_event_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            send_text_message(reply_token, "yes")
        elif year == 19:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(year + "\n" + green_people + "\n" + green_rate + "\n" + blue_people + "\n" + blue_rate)
        f.close()

    def is_going_to_no_event_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_no_event_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'w')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            send_text_message(reply_token, "yes")
        elif year == 19:
            send_text_gessage(reply_token, "no")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(year + "\n" + green_people + "\n" + green_rate + "\n" + blue_people + "\n" + blue_rate)
        f.close()

