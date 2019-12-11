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
        send_text_message(reply_token, "遊戲目的：幫助蔡英文贏得2020總統大選\n遊玩方式：\n在面臨選擇時輸入是/否\n其餘時候輸入繼續")

    def is_going_to_16_18(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_16_18(self, event):
        reply_token = event.reply_token
        f = open("gamedata.txt", "r")
        send_text_message(reply_token, "西元：           20" + f.readline() +
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
            send_text_message(reply_token, "反年改團體正走上街頭進行抗爭，情況愈演愈烈，警民衝突隨時可能爆發，是否要向反年改團體妥協呢？")

    def is_going_to_kaohsiung(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and (year == 18)

    def on_enter_kaohsiung(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "高雄市長選舉到了，儘管陳其邁的對手看起來像個跳梁小丑，但其邁仍然沒有必勝的把握，黨中央是否要發動動員令來幫助其邁呢？")

    def is_going_to_fish_win(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_fish_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r+')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        green_people -= 300000
        green_rate -= 2
        blue_people += 200000
        blue_rate += 3
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        send_text_message(reply_token, "韓國瑜勝選了，這對於整個綠營無疑是個巨大的打擊，除此之外，拿下一個綠營的重要城市，使得藍營的士氣空前地高漲")

    def is_going_to_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "西元：           20" + f.readline() +
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
            send_text_message(reply_token, "韓國瑜請假參選總統，並向蔡英文發出邀請，要蔡英文和他一起請假參選，是否要接受他的邀請呢？")
        elif year == 19:
            send_text_message(reply_token, "香港的警民衝突愈加嚴重，是否要在公開場合發表支持香港的言論呢？")

    def is_going_to_battle_win(self, event):
        text = event.message.text
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        return (text.lower() == "繼續") and (year == 20)

    def on_enter_battle_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')

        send_text_message(reply_token, "2020總統大選正式開始，究竟誰能獲得最後的勝利呢？")
        
    def is_going_to_fish_lose(self, event):
        text = event.message.text
        return text.lower() == "是"

    def on_enter_fish_lose(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "韓國瑜敗選了，但這對於藍綠兩黨而言都是一件再正常不過的事情。")

    def is_going_to_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "繼續"

    def on_enter_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "西元：           20" + f.readline() +
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
            send_text_message(reply_token, "敗選的韓國瑜發表了演說，他的死忠支持者人數逐日攀升，看來是打算趁著這股氣勢和蔡英文角逐總統呢！是否要發動輿論揭發他的醜聞呢？")
        elif year == 19:
            send_text_message(reply_token, "香港的警民衝突愈加嚴重，是否要在公開場合發表支持香港的言論呢？")

    def is_going_to_battle_lose(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
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
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and ((green_people * green_rate)) > (blue_people * blue_rate)


    def on_enter_result_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "蔡英文成功連任！")
        self.go_back()
        
    def is_going_to_result_lose(self, event):
        text = event.message.text
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        return (text.lower() == "繼續") and ((green_people * green_rate)) < (blue_people * blue_rate)

    def on_enter_result_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        send_text_message(reply_token, "韓國瑜勝選，台灣進入黑暗時代！")
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
            green_people += 400000
            green_rate += 3
            blue_people += 100000
            blue_rate += 1
            send_text_message(reply_token, "蔡英文政府不顧財團利益，繼續推動一例一休，雖然得罪了財團，卻贏得了民心。")
        elif year == 17:
            green_people -= 100000
            green_rate -= 1
            send_text_message(reply_token, "蔡英文政府向反年改團體妥協，令許多綠營人士相當失望，而反年改團體因本質貪得無厭，並無投靠綠營的趨勢。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_no_event_16_18(self, event):
        text = event.message.text
        return text.lower() == "否"
    
    def on_enter_no_event_16_18(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 16:
            green_people -= 200000
            green_rate -= 2
            send_text_message(reply_token, "蔡英文政府向財團妥協，民調開始下滑。")
        elif year == 17:
            green_people += 150000
            green_rate += 2
            send_text_message(reply_token, "蔡英文政府持續推動反年改，獲得年輕族群認同。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_yes_event_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "是"
        
    def on_enter_yes_event_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            green_people -= 200000
            green_rate -= 4
            send_text_message(reply_token, "蔡英文總統決定和韓國瑜一起請假選總統，不得不說，這實在是個愚蠢的決定。")
        elif year == 19:
            green_people += 300000
            green_rate += 5
            blue_people += 100000
            blue_rate += 2
            send_text_message(reply_token, "蔡英文總統公開支持香港抗爭，引起藍營人士不滿，卻吸引了更多年輕族群的目光。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_no_event_18_20_win(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_no_event_18_20_win(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            green_people += 200000
            green_rate += 1
            blue_people -= 100000
            blue_rate -= 1
            send_text_message(reply_token, "蔡英文總統公開拒絕了韓國瑜的邀請，並語中帶刺地稍稍反擊了對方。韓國瑜的低能行徑使得部份中間選民選擇靠向綠營。")
        elif year == 19:
            green_people -= 100000
            green_rate -= 1
            send_text_message(reply_token, "蔡英文總統拒絕對香港抗爭一事做出正面回應，使得年輕人相當失望。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_yes_event_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "是"

    def on_enter_yes_event_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            green_people += 300000
            green_rate += 3
            blue_people -= 100000
            blue_rate += 5
            send_text_message(reply_token, "愈多愈多媒體開始抨擊韓國瑜，造成其聲望逐漸下降，但其死忠支持者一再生命全國上下都在卡韓，更堅定了他們的決心。")
        elif year == 19:
            green_people += 300000
            green_rate += 5
            blue_people += 100000
            blue_rate += 2
            send_text_message(reply_token, "蔡英文總統公開支持香港抗爭，引起藍營人士不滿，卻吸引了更>多年輕族群的目光。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

    def is_going_to_no_event_18_20_lose(self, event):
        text = event.message.text
        return text.lower() == "否"

    def on_enter_no_event_18_20_lose(self, event):
        reply_token = event.reply_token
        f = open('gamedata.txt', 'r')
        year = int(f.readline())
        green_people = int(f.readline())
        green_rate = int(f.readline())
        blue_people = int(f.readline())
        blue_rate = int(f.readline())
        f.close()
        if year == 18:
            blue_people += 200000
            send_text_message(reply_token, "韓國瑜的聲望愈加高漲。")
        elif year == 19:
            green_people -= 100000
            green_rate -= 1
            send_text_gessage(reply_token, "蔡英文總統拒絕對香港抗爭一事做出正面回應，使得年輕人相當>失望。")
        year += 1
        f = open('gamedata.txt', 'w')
        f.write(str(year) + "\n" + str(green_people) + "\n" + str(green_rate) + "\n" + str(blue_people) + "\n" + str(blue_rate))
        f.close()

