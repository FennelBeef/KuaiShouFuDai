import time

from Operation import Operation


class Choujiang:
    def zhaofudai(self):
        operation = Operation()
        d = operation.get_device()  # 获取设备并返回
        while True:
            zhibojian_pic = operation.get_Screenshot(d, "zhibojian_pic")  # 获取手机截图
            operation.crop_pic(0, 0, 1077, 443, "zhibojian_pic", "zhibojian_cut_pic")
            found, locations = operation.multi_scale_template_matching("pic/zhibojian_cut_pic.png",
                                                                       "pic/fudai.png")  # 根据直播间截图匹配是否存在福袋
            if found:
                print("该直播间存在福袋")
                operation.click_locations(locations, d)  # 点击福袋位置
                operation.get_Screenshot(d, "fudai_Content")  # 点击福袋后的2级页面
                operation.convert_to_grayscale("fudai_Content")
                fudai_time = operation.check_time(d)
                fudai_neirong = operation.check_neirong(d)
                print(f"{fudai_time}秒后开奖")
                print(f"福袋内容：{fudai_neirong}")
                if int(fudai_time) >= 300:  # 福袋等待时间小于5分钟
                    print("福袋等待时间大于5分钟，等待中")
                    time.sleep(fudai_time - 300)  # 等待中奖时间
                    fudai_time = 300

                if int(fudai_time) <= 300:  # 福袋等待时间小于5分钟
                    if operation.click_choujiang():
                        print("点击参与，等待开奖")
                        time.sleep(fudai_time + 5)  # 等待中奖时间
                        WinResult = operation.check_WinResult(d)
                        if "本轮未中奖" in WinResult:
                            print("本轮未中奖,将参与下一次中奖")
                            d.keyevent(4)
                            continue
                        else:
                            print("恭喜，成功中奖！")
                            break


                    else:
                        print("福袋任务过于复杂，跳过")
                        break
