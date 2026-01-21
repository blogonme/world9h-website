#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译新闻文章到中文
"""

import os
import re

# 新闻页面翻译映射
news_translations = {
    # === 新闻中心页面标题 ===
    'News about comodity trade': '大宗商品贸易新闻',
    'The latest logistics service news, learn more about us.': '最新物流服务资讯，了解更多关于我们。',
    'Real-time news': '实时新闻',
    
    # === 第一篇文章：美墨玉米贸易争端 ===
    'US escalates Mexico corn trade spat with dispute panel request': '美国就玉米贸易争端向墨西哥提出仲裁请求',
    'WASHINGTON, Aug 17 (Reuters) - The United States on Thursday escalated its objections to Mexico\'s curbs on genetically modified corn imports, requesting a dispute settlement panel under the North American trade pact, the U.S. Trade Representative\'s office said.': '华盛顿8月17日（路透社）- 美国贸易代表办公室周四表示，美国加大了对墨西哥限制转基因玉米进口的反对力度，根据北美贸易协定请求设立争端解决小组。',
    'The request to send the dispute to arbitrators was announced after formal consultations failed to resolve deep divisions between the two close trading partners over use of genetically modified (GM) corn, widely produced by U.S. farmers.': '在双方就转基因玉米使用问题的正式磋商未能解决两个密切贸易伙伴之间的深刻分歧后，美方宣布将争端提交仲裁员。转基因玉米在美国农民中被广泛种植。',
    'Mexico\'s Economy Ministry said it would defend its GM corn policies before the dispute panel, saying on the social media platform X that they "are consistent with trade obligations."': '墨西哥经济部表示将在争端小组面前捍卫其转基因玉米政策，并在社交媒体平台X上表示这些政策"符合贸易义务"。',
    'Washington alleges that Mexico\'s decree banning imports of GM corn used in dough and tortillas for human consumption is not based on science and violates its commitments under the U.S.-Mexico-Canada Agreement on trade launched in 2020.': '华盛顿指控墨西哥禁止进口用于面团和玉米饼人类食用的转基因玉米的法令不是基于科学的，违反了其在2020年启动的美墨加贸易协定下的承诺。',
    'If the panel rules in favor of the U.S. and Mexico fails to comply with its directives, USTR could ultimately win the right to impose punitive tariffs on Mexican goods, which could spark a rare North American trade war.': '如果小组裁定美国胜诉而墨西哥未能遵守其指令，美国贸易代表可能最终赢得对墨西哥商品征收惩罚性关税的权利，这可能引发罕见的北美贸易战。',
    'U.S. Trade Representative Katherine Tai said in a statement that the move was aimed at enforcing Mexico\'s USMCA obligations to maintain science-based regulations on agricultural biotechnology.': '美国贸易代表凯瑟琳·戴在一份声明中表示，此举旨在执行墨西哥在美墨加协定下维持基于科学的农业生物技术法规的义务。',
    '"It is critical that Mexico eliminate its USMCA-inconsistent biotechnology measures so that American farmers can continue to access the Mexican market and use innovative tools to respond to climate and food security challenges," Tai said.': '戴说："墨西哥消除其与美墨加协定不一致的生物技术措施至关重要，这样美国农民才能继续进入墨西哥市场，并使用创新工具应对气候和粮食安全挑战。"',
    'Mexico now buys about $5 billion worth of U.S. GM corn annually, mostly for livestock feed. It says biotech corn harms native varieties and may have adverse health effects, an assertion that the U.S. side disputes.': '墨西哥目前每年购买约50亿美元的美国转基因玉米，主要用于牲畜饲料。墨西哥表示，生物技术玉米会损害本土品种并可能对健康产生不利影响，但美方对此表示异议。',
    'Mexico\'s also plans to ban the herbicide glyphosate, which it considers dangerous amid lawsuit settlements with cancer patients despite regulators worldwide determining its safety. Many GM corn varieties are modified to tolerate the herbicide.': '墨西哥还计划禁止除草剂草甘膦，尽管全球监管机构已确定其安全性，但墨西哥认为它是危险的，因为有与癌症患者达成的诉讼和解。许多转基因玉米品种被改造为能够耐受这种除草剂。',
    'Canada\'s Trade Ministry, which has sided with U.S. concerns about Mexico\'s corn policies, "is considering its next steps," a spokesperson said, adding Trade Minister Mary Ng "has consistently been clear about the importance of maintaining science-based approaches to biotechnology approvals."': '加拿大贸易部站在美国一边对墨西哥的玉米政策表示关切，一位发言人表示该部"正在考虑下一步行动"，并补充说贸易部长黄宝仪"一直明确表示维持基于科学的生物技术审批方法的重要性"。',
    'Corn futures temporarily pared gains at the Chicago Board of Trade after USTR\'s announcement as traders worried the spat could threaten U.S. exports to Mexico.': '美国贸易代表办公室宣布后，芝加哥期货交易所的玉米期货一度缩减涨幅，交易商担心争端可能威胁美国对墨西哥的出口。',
    'FRUITLESS CONSULTATIONS': '无果的磋商',
    'The panel request follows 75 days of formal consultations&nbsp;requested by U.S. officials&nbsp;in June. Mexico has sought U.S. cooperation to jointly conduct scientific research on the health impacts of genetically modified corn, but Mexican officials&nbsp;told Reuters on Aug. 3&nbsp;that their U.S. counterparts denied the request.': '此次小组请求是在美国官员于6月提出的为期75天的正式磋商之后。墨西哥曾寻求美国合作共同进行转基因玉米健康影响的科学研究，但墨西哥官员8月3日告诉路透社，他们的美国同行拒绝了这一请求。',
    '"Mexico\'s approach to biotechnology is not based on science and runs counter to decades\' worth of evidence demonstrating its safety and the rigorous, science-based regulatory review system that ensures it poses no harm to human health and the environment," U.S. Agriculture Secretary Tom Vilsack said in the statement.': '美国农业部长汤姆·维尔萨克在声明中说："墨西哥对生物技术的做法不是基于科学的，与数十年来证明其安全性的证据以及确保其对人类健康和环境无害的严格的、基于科学的监管审查系统背道而驰。"',
    'He added that innovations in agricultural biotechnology to enhance yields also help ease challenges on global food and nutrition security, climate change and food price inflation.': '他补充说，提高产量的农业生物技术创新也有助于缓解全球粮食和营养安全、气候变化和食品价格通胀方面的挑战。',
    'USTR\'s decision drew cheers from U.S. corn trade groups and U.S. lawmakers from both parties, who say Mexico\'s policies were hurting U.S. farmers.': '美国贸易代表的决定受到美国玉米贸易团体和两党国会议员的欢迎，他们表示墨西哥的政策正在伤害美国农民。',
    '"U.S. officials have exhausted every avenue trying to resolve this conflict and are left with no other choice but to turn to a third-party panel in hopes of quickly rectifying this issue," National Corn Growers Association Tom Haag said in a statement. "We are deeply appreciative of USTR for standing up for America&rsquo;s corn growers."': '全国玉米种植者协会的汤姆·哈格在一份声明中说："美国官员已经用尽一切途径试图解决这一冲突，别无选择只能求助于第三方小组，希望能迅速纠正这一问题。我们非常感谢美国贸易代表为美国玉米种植者挺身而出。"',
    'Republican Senator Deb Fischer of Nebraska said the move would "hold Mexico accountable and prevent its blatant trade violation under the USMCA."': '内布拉斯加州共和党参议员黛布·费舍尔表示，此举将"让墨西哥承担责任，阻止其公然违反美墨加协定的贸易行为。"',
    'Under USMCA\'s&nbsp;dispute settlement rules, a five-person panel, chosen from a roster of pre-approved experts, must be convened within 30 days, with a chair jointly chosen and the U.S. side choosing two Mexican panelists and Mexico choosing two American panelists. The panel will review testimony and written submissions and its initial report is due 150 days after the panel is convened.': '根据美墨加协定的争端解决规则，必须在30天内从预先批准的专家名单中选出五人小组召开会议，主席由双方共同选择，美方选择两名墨西哥小组成员，墨西哥选择两名美国小组成员。小组将审查证词和书面意见，初步报告将在小组召开后150天内提交。',
    'Previous USMCA dispute panels last year ruled in the U.S.\'s favor in a dispute over&nbsp;Canadian dairy quotas, and against the U.S. on&nbsp;automotive rules of origin, siding with Mexico and Canada.': '去年的美墨加协定争端小组曾在加拿大乳制品配额争端中裁定美国胜诉，在汽车原产地规则争端中裁定美国败诉，站在墨西哥和加拿大一边。',
    'There have been other disagreements between the U.S. and Mexico, most notably over energy in which the U.S. has argued that Mexico\'s nationalist policy prejudices foreign companies.': '美国和墨西哥之间还存在其他分歧，最显著的是能源问题，美国认为墨西哥的民族主义政策损害了外国公司的利益。',

    # === 第二篇文章：巴西JBS对中国仍保持乐观 ===
    'Brazil\'s JBS remains optimistic on China despite short-term woes': '巴西JBS对中国市场仍保持乐观态度',
    'Speaking at an industry event on Thursday, JBS CEO Gilberto Tomazoni said he still believes Chinese beef consumption will rise over time as eating that kind of protein is &ldquo;aspirational&rdquo; in Chinese society.': '周四在一次行业活动上发言时，JBS首席执行官吉尔伯托·托马佐尼表示，他仍然相信中国牛肉消费量会随着时间推移而增加，因为在中国社会，吃这种蛋白质是一种"令人向往"的事情。',
    'He said five years ago China&rsquo;s per capita beef consumption was about 5 kg (11 pounds) whereas now it is around 7 to 7.5 kg (15 to 17 pounds).': '他说，五年前中国人均牛肉消费量约为5公斤（11磅），而现在约为7至7.5公斤（15至17磅）。',
    '&ldquo;When pork prices became cheap again in China, there was no change in the beef curve,&rdquo; he said. &ldquo;Beef consumption in China will rise in the long run.&rdquo;': '"当中国猪肉价格再次变得便宜时，牛肉曲线没有变化，"他说。"从长远来看，中国的牛肉消费量将会上升。"',
    'However, Brazilian beef exports to China in the first half fell 29% to $2.6 billion, and by volume the drop was 5% to 512,306 metric tons, trade data shows.': '然而，贸易数据显示，上半年巴西对中国的牛肉出口下降了29%，至26亿美元，出口量下降了5%，至512,306公吨。',
    'Eduardo Miron, the chief executive of family-owned Brazilian beefpacker Frigol, said at the same event that the slump is cause for concern. He also worries about currently low domestic consumption and exporters&rsquo; dependence &ldquo;on a single importer,&rdquo; referring to China.': '家族企业巴西牛肉加工商Frigol的首席执行官爱德华多·米隆在同一活动上表示，这种下滑令人担忧。他还担心目前国内消费低迷以及出口商对"单一进口商"（指中国）的依赖。',
    'According to a U.S. Department of Agriculture (USDA) report issued in March, Chinese demand in 2022 accounted for 64% of total Brazilian beef exports. The closest beef export destination for Brazil was the United States, with a 7.6% chunk.': '根据美国农业部3月发布的一份报告，2022年中国需求占巴西牛肉出口总量的64%。巴西最接近的牛肉出口目的地是美国，占7.6%。',
    'In 2023, China&rsquo;s beef imports may fall because its domestic output is expected to increase, said the USDA.': '美国农业部表示，2023年中国牛肉进口可能会下降，因为其国内产量预计会增加。',
    '&ldquo;After the end of lockdowns, the mad-cow related ban, we had the impression (China&rsquo;s) demand would be as strong as in 2022,&rdquo; said Miron, who was previously Marfrig&rsquo;s chief executive and worked for Cargill. &ldquo;We all got surprised.&rdquo;': '"在封锁结束、疯牛病相关禁令解除后，我们以为（中国的）需求会像2022年一样强劲，"曾担任Marfrig首席执行官并在嘉吉工作过的米隆说。"我们都感到惊讶。"',
    'For meatpackers like Frigol, which only produces beef in Brazil, risks may be greater than for more globalized rivals.': '对于像Frigol这样只在巴西生产牛肉的肉类加工企业来说，风险可能比更加全球化的竞争对手更大。',
    '&ldquo;As the Brazilian cattle production cycle reaches its peak, the growing availability of cattle will pressure animal and beef prices downwards this year,&rdquo; the USDA said.': '"随着巴西牛群生产周期达到高峰，牛群供应的增加将在今年给动物和牛肉价格带来下行压力，"美国农业部表示。',

    # === 第三篇文章：印度大米出口禁令 ===
    'Rice export ban:Why India is so crucial to global rice trade': '大米出口禁令：为什么印度对全球大米贸易至关重要',
    'India accounts for more than 40% of global rice exports': '印度占全球大米出口的40%以上',
    'The Indian government Thursday prohibited the export of non-basmati white rice with immediate effect this was seemingly in response to both a rise in domestic prices and decreased sowing in several key rice-producing states because of erratic monsoon. According to food ministry&nbsp;data, the retail price of the grain climbed about 15% &nbsp;in Delhi this year while the average nationwide price gained more than 8%.': '印度政府周四立即禁止出口非印度香米白米，这似乎是为了应对国内价格上涨以及由于季风不稳定导致几个主要产米邦播种面积减少。根据食品部的数据，今年德里大米零售价格上涨了约15%，全国平均价格上涨了8%以上。',
    'Shipments will be allowed on the basis of permission granted by the government to other countries to meet their food security needs and based on request of their governments, the notification said.&nbsp;': '通知称，将根据政府向其他国家授予的许可以满足其粮食安全需求，以及根据这些国家政府的请求来允许出口。',
    'The latest Indian government move, which has already imposed restrictions on wheat and sugar exports, would affect a large portion of global rice trade. Rice is a staple food for about half of the world&rsquo;s population, with Asia consuming about 90% of global supply.&nbsp;': '印度政府最新举措已经对小麦和糖出口实施了限制，这将影响全球大米贸易的很大一部分。大米是世界约一半人口的主食，亚洲消费了全球供应量的约90%。',
    'Why India is crucial to the global rice trade': '为什么印度对全球大米贸易至关重要',
    'India accounts for more than 40% of global rice exports, which amounted to 55.4 million metric tons in 2022. India\'s rice shipments in 2022 were more than the combined shipments of the Thailand, Vietnam, Pakistan and the US, the next four big exporters of the grain.': '印度占全球大米出口的40%以上，2022年全球大米出口达到5540万公吨。印度2022年的大米出口量超过了泰国、越南、巴基斯坦和美国这四个主要出口国的出口总和。',
    'Over 140 countries are net importers of India non-basmati rice. Benin, Bangladesh, Angola, Cameroon, Djibouti, Guinea, Ivory Coast, Kenya and Nepal, having rice a staple food, are key buyers of non-basmati Indian rice.': '超过140个国家是印度非印度香米的净进口国。贝宁、孟加拉国、安哥拉、喀麦隆、吉布提、几内亚、科特迪瓦、肯尼亚和尼泊尔等以大米为主食的国家是印度非印度香米的主要买家。',
    'India exported 17.86 million tons of non-basmati rice in 2022. In September 2022, Indian government banned the exports of broken rice and imposed a 20% duty on exports of various grades of rice as the country was itself grappling with high prices of food grains.&nbsp;': '2022年印度出口了1786万吨非印度香米。2022年9月，印度政府禁止出口碎米，并对各等级大米出口征收20%的关税，因为该国本身正在应对粮食价格高企的问题。',
    'The Indian government has not put any restrictions on the export of basmati rice which stood at 4.4 million tons in 2022. Iran, Iraq and Saudi Arabia mainly buy premium basmati rice from India.': '印度政府没有对印度香米出口实施任何限制，2022年印度香米出口量为440万吨。伊朗、伊拉克和沙特阿拉伯主要从印度购买优质印度香米。',
    'Indian farmers plant paddy rice twice in a year. Summer-sown crop planting starting in June accounts for more than 80% of the total output, which was 135.5 million tons in the 2022/23 crop year. In winter months, paddy rice is mainly cultivated in central and southern states.': '印度农民每年种植两季水稻。从6月开始的夏播作物种植占总产量的80%以上，2022/23作物年总产量为1.355亿吨。在冬季，水稻主要在中部和南部各邦种植。',
    'Monsoon: The late arrival of the monsoon led to a large rain deficit up to mid-June. And while heavy rains since the last week of June have erased the shortfall, they have caused significant damage to crops. The area under paddy could drop marginally in 2023 because of erratic monsoon rainfall distribution.': '季风：季风迟到导致6月中旬之前降雨严重不足。虽然6月最后一周以来的暴雨消除了缺口，但也对农作物造成了重大损害。由于季风降雨分布不稳定，2023年水稻种植面积可能会略有下降。',

    # === 第四篇文章：谷物期货与俄乌局势 ===
    'Grain futures calm down but Russia-Ukraine supplies more precarious than ever': '谷物期货趋于平静，但俄乌供应更加岌岌可危',
    'Maksym Belchenko/iStock via Getty Images': '图片来源：Maksym Belchenko/iStock via Getty Images',
    'Wheat futures on the Chicago Board of Trade swung between losses and gains before finishing flat Thursday, providing hope that crop markets are starting to settle down after Russia\'s escalation of the war in Ukraine.': '芝加哥期货交易所的小麦期货周四在涨跌之间摇摆，最终收平，这让人们看到了农作物市场在俄罗斯升级乌克兰战争后开始稳定下来的希望。',
    'U.S. wheat had surged more than&nbsp;11% in the previous two sessions as Russia pulled out of the Ukraine grain deal, which will force supplies to world markets through narrower and more cumbersome avenues.': '此前两个交易日，美国小麦已飙升超过11%，原因是俄罗斯退出了乌克兰谷物协议，这将迫使向世界市场的供应通过更窄更繁琐的渠道进行。',
    'Both countries warned that ships headed to each other\'s ports could be considered military targets, marking a&nbsp;new phase of the conflict&nbsp;that began in February 2022.': '两国都警告称，驶往对方港口的船只可能被视为军事目标，标志着2022年2月开始的冲突进入了新阶段。',
    'Ukraine has increased reliance on its Danube River ports and rail and road routes via the European Union throughout the war, but a heatwave fanning across part of southern Europe is lowering river levels and restricting export capacity, which&nbsp;will make shipping grain even more difficult.': '整个战争期间，乌克兰越来越依赖其多瑙河港口以及通过欧盟的铁路和公路路线，但席卷南欧部分地区的热浪正在降低河流水位并限制出口能力，这将使粮食运输更加困难。',
    'Cutting off the Black Sea ports will cut Ukraine\'s monthly export capacity from 7M-8M tons to a maximum of ~4M tons, according to Argus Media agriculture analyst Alexandre Marie.': '据Argus Media农业分析师亚历山大·玛丽称，切断黑海港口将使乌克兰的月出口能力从700-800万吨降至最多约400万吨。',
    'CBOT wheat futures (W_1:COM) for September delivery ended virtually unchanged at $7.27 1/2 per bushel, while December corn (C_1:COM) closed&nbsp;-1.3%&nbsp;to $5.46 per bushel and November soybeans (S_1:COM) settled&nbsp;-0.3%&nbsp;at $14.03 1/4 per bushel, with forecasts predicting wetter weather in the Corn Belt over the weekend.': 'CBOT 9月交割小麦期货(W_1:COM)收盘基本持平于每蒲式耳7.27.5美元，12月玉米(C_1:COM)收跌1.3%至每蒲式耳5.46美元，11月大豆(S_1:COM)收跌0.3%至每蒲式耳14.03.25美元，预报显示周末玉米带天气将更加湿润。',
    'ETFs: (NYSEARCA:WEAT), (CORN), (SOYB), (DBA), (MOO)': 'ETF代码：(NYSEARCA:WEAT), (CORN), (SOYB), (DBA), (MOO)',
    'The drop in CBOT grain futures was linked to a wetter weather outlook for the next few days.': 'CBOT谷物期货下跌与未来几天天气将更加湿润的预期有关。',
    'Ag research firm DTN forecasts isolated and scattered showers in growing areas over the weekend, although conditions are expected to turn back toward hot and dry next week.': '农业研究公司DTN预测周末种植区将出现零星阵雨，但预计下周天气将再次转为炎热干燥。',

    # === 第五篇文章：上海清算所数字人民币服务 ===
    'Shanghai Clearing House launches digital yuan services for commodity trading': '上海清算所推出大宗商品交易数字人民币服务',
    'Fast facts': '快讯',
    'The services allow users to make cross-bank clearings and settlements on commodities with the digital yuan, according to a Monday&nbsp;announcement&nbsp;by the Shanghai Clearing House, which handles bonds, interest rates, foreign exchange, credit, and commodities.': '据上海清算所周一公告，该服务允许用户使用数字人民币进行大宗商品的跨行清算和结算。上海清算所处理债券、利率、外汇、信贷和大宗商品业务。',
    'The services could improve the security and cost effectiveness of cross-border settlements of commodities, and boost the internationalization of China&rsquo;s currency, Dong Dengxin, director of the Finance and Securities Institute of the Wuhan University of Science and Technology, said in a Global Times&nbsp;report&nbsp;on Sunday.': '武汉科技大学金融证券研究所所长董登新周日在《环球时报》的一篇报道中表示，该服务可以提高大宗商品跨境结算的安全性和成本效益，并推动人民币国际化。',
    'Shanghai Clearing House&rsquo;s move is not the digital yuan&rsquo;s first use in commodity trading. In October 2022, Shandong International Commodity Exchange facilitated a 1 million yuan&nbsp;settlement&nbsp;on imported rubber with digital yuan, the first digital yuan commodity trading use case in the city of Qingdao, China.': '上海清算所的这一举措并非数字人民币在大宗商品交易中的首次应用。2022年10月，山东国际商品交易所使用数字人民币完成了100万元进口橡胶结算，这是中国青岛市首个数字人民币大宗商品交易应用案例。',
    'China&rsquo;s CBDC pilot is also spreading in retail usage. On June 20, Qingdao city&nbsp;launched&nbsp;the country&rsquo;s first digital yuan payments for urban rail transit fees, where users pay from digital yuan hard wallets embedded in their SIM cards.': '中国央行数字货币试点也在零售领域推广。6月20日，青岛市推出全国首个城市轨道交通数字人民币支付服务，用户可以使用嵌入SIM卡的数字人民币硬钱包支付。',
    'Also on June 20,&nbsp;JD.com, one of China&rsquo;s leading online shopping platforms,&nbsp;said&nbsp;it saw a 254% increase in the number of digital yuan transactions during the 618 Festival &ndash; a shopping festival started in 2010 and taking place from late May to June 18 &ndash; from the same period last year, with transaction amounts breaking the record, according to the company.': '同样在6月20日，中国领先的在线购物平台京东表示，618购物节（该节日始于2010年，从5月下旬到6月18日举行）期间数字人民币交易数量同比增长254%，交易金额创下新高。',
    'However, JD.com did not disclose the exact amount of total or digital yuan transactions during the Festival. Chinese e-commerce platforms had a relatively&nbsp;quiet 618 session&nbsp;this year amid an economic slowdown.': '然而，京东没有披露购物节期间总交易额或数字人民币交易的确切金额。在经济放缓的背景下，中国电商平台今年的618购物节相对较为平静。',
}

# 需要翻译的文件列表
files_to_translate = [
    'zh/Logistics.html',
    'zh/4/2/1313559.html',
    'zh/4/2/1334296.html',
    'zh/4/2/1334299.html',
    'zh/4/2/1360287.html',
    'zh/4/2/1360288.html',
    'zh/index.html',  # 首页也有新闻摘要
]

def translate_file(filepath):
    """翻译单个文件"""
    print(f"正在翻译: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 执行所有翻译替换
    for eng, chn in news_translations.items():
        content = content.replace(eng, chn)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"完成: {filepath}")

# 翻译所有文件
for filepath in files_to_translate:
    if os.path.exists(filepath):
        translate_file(filepath)
    else:
        print(f"文件不存在: {filepath}")

print("\n新闻文章翻译完成！")
