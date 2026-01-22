#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复中文首页的编码问题和翻译
"""

import re

# 读取英文版作为基础
with open('world9h.com/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义替换规则：英文 -> 中文
replacements = [
    # 标题和公司名
    ('The Nine International Supply Chain', '九鸿国际供应链管理有限公司'),
    ('THE NINE INTERNATIONAL SUPPLY CHAIN', '九鸿国际供应链管理有限公司'),
    
    # 菜单项
    ('>HOME<', '>首页<'),
    ('>INDEX<', '>首页<'),
    ('>ABOUT US<', '>关于我们<'),
    ('>SERVICE<', '>业务范围<'),
    ('>CONTACT US<', '>联系我们<'),
    ('>NEWS<', '>新闻中心<'),
    ('>News<', '>新闻中心<'),
    
    # 按钮
    ('>LEARN MORE<', '>了解更多<'),
    ('>CONTACT US<', '>联系我们<'),
    
    # 口号和标语
    ('Efficiency, Integrity, and Prosperity in Trade', '高效、诚信、贸易繁荣'),
    ('Connecting Markets, Empowering Trade', '连接市场，赋能贸易'),
    ('Unlocking Opportunities in the Global Marketplace', '开启全球市场机遇'),
    
    # 服务区块
    ('>Service<', '>业务范围<'),
    ('Provide professional commodity trading services for our customers.', '为客户提供专业的大宗商品贸易服务。'),
    
    # 服务项目
    ('>01 Commodity Trade<', '>01 大宗商品贸易<'),
    ('>02 ILC<', '>02 国际信用证<'),
    ('At The Nine International Supply Chain, we excel in international commodity trading, sourcing high-quality materials and providing seamless solutions across sectors including iron ore, coal, agricultural commodities, and maritime shipping. Trust us as your reliable partner to unlock the potential of global trade.', 
     '香港九鸿供应链管理有限公司在国际大宗商品贸易领域表现卓越，采购优质原材料，并在铁矿石、煤炭、农产品和海运等多个领域提供无缝解决方案。信赖我们作为您可靠的合作伙伴，开启全球贸易的无限潜力。'),
    ('We specialize in international letter of credit services, ensuring secure and efficient trade transactions by managing the complexities of opening and managing letters of credit, navigating international trade regulations with expertise.',
     '我们专注于国际信用证服务，专业管理信用证的开立和运营复杂流程，确保贸易交易安全高效，熟练掌握国际贸易法规。'),
    
    # 数据统计
    ('>Customs and customer satisfaction<', '>客户满意度<'),
    ('>Logistics of transactions<', '>交易物流<'),
    ('>Fast customs clearance<', '>快速清关<'),
    
    # 新闻区块
    ('>LATEST NEWS<', '>最新动态<'),
    ('The latest commodity trade service news, learn more about us.', '最新大宗商品贸易服务资讯，了解更多关于我们。'),
    
    # 页脚
    ('>Services<', '>业务范围<'),
    ('>Commodity Trade<', '>大宗商品贸易<'),
    ('>ILC<', '>国际信用证<'),
    ('>Contact Us<', '>联系我们<'),
    ('>Subscribe<', '>订阅<'),
    ('Enter your email', '输入您的邮箱'),
    ('>Subscribe<', '>订阅<'),
    ('>      Subscribe<', '>      订阅<'),
    ('Subscribe\n', '订阅\n'),
    ('All Rights Reserved', '版权所有'),
    
    # 搜索框 (修复乱码)
    ('璇疯緭鍏ュ叧閿瘝', '请输入关键词'),
    ('鎼滅储', '搜索'),
    
    # 修复底部版权乱码
    ('涔濋椿鍦嬮殯渚涙噳閺?', '九鸿国际供应链'),
    ('铏瓙寤虹珯', '虫子建站'),
    
    # 主要介绍内容
    ('Experience the unrivaled excellence of The Nine International Supply Chain(The Nine H International Trading Pte. Ltd. , The Nine International Supply Chain Management Group Holdings Limited.): International Tamrading. We offer the best-in-class solutions for global commodity trading, international letter of credit, and standby letter of credit, providing the utmost convenience, security, and profitability for your business. Our cutting-edge services ensure seamless transactions, risk mitigation, and unparalleled trade facilitation.',
     '体验九鸿国际供应链管理有限公司（九鸿国际贸易有限公司，九鸿国际供应链管理集团控股有限公司）无与伦比的卓越服务：国际贸易。我们为全球大宗商品贸易、国际信用证和备用信用证提供一流的解决方案，为您的业务带来极致便利、安全和盈利能力。我们的尖端服务确保无缝交易、风险缓释和无与伦比的贸易便利化。'),
    
    ('At The Nine International Supply Chain, we are a prominent player in international commodity trading, offering comprehensive services across various sectors. With expertise in iron ore, coal, agricultural commodities, and maritime shipping, we provide seamless and professional solutions to meet our clients\' diverse needs.',
     '九鸿国际供应链管理有限公司是国际大宗商品贸易领域的知名企业，在各个领域提供全面的服务。凭借在铁矿石、煤炭、农产品和海运方面的专业知识，我们提供无缝且专业的解决方案，以满足客户的多样化需求。'),
    
    ('Our iron ore and coal trading division sources high-quality materials from global mines, ensuring compliance with international standards. From bulk shipments to smaller quantities, we prioritize competitive pricing and timely delivery.',
     '我们的铁矿石和煤炭贸易部门从全球矿山采购优质材料，确保符合国际标准。从散货运输到小批量出货，我们优先考虑有竞争力的价格和及时的交付。'),
    
    ('In the agricultural commodities segment, we specialize in importing frozen chicken feet, white sugar, and corn. With strict quality control measures, we maintain freshness and adhere to global food safety regulations.',
     '在农产品领域，我们专注于进口冷冻鸡爪、白糖和玉米。通过严格的质量控制措施，我们保持新鲜度并遵守全球食品安全法规。'),
    
    ('Additionally, we provide international letter of credit services, facilitating secure and efficient trade transactions. Our deep understanding of trade regulations ensures seamless management of letters of credit.',
     '此外，我们提供国际信用证服务，促进安全高效的贸易交易。我们对贸易法规的深刻理解确保了信用证的无缝管理。'),
    
    ('Moreover, our maritime shipping services offer efficient transportation solutions. Partnering with trusted shipping companies, we streamline logistics and ensure reliable delivery.',
     '此外，我们的海运服务提供高效的运输解决方案。与值得信赖的航运公司合作，我们简化物流并确保可靠的交付。'),
    
    ('With our industry expertise, global network, and commitment to customer satisfaction, we are a trusted partner in international commodity trading. Choose The Nine International Supply Chain for expertise in iron ore, coal, agricultural commodities, and maritime shipping, and unlock the full potential of global trade.',
     '凭借我们的行业专长、全球网络和对客户满意度的承诺，我们是国际大宗商品贸易中值得信赖的合作伙伴。选择香港九鸿供应链管理有限公司，获取铁矿石、煤炭、农产品和海运方面的专业知识，释放全球贸易的全部潜力。'),
]

# 执行替换
for old, new in replacements:
    content = content.replace(old, new)

# 修复路径 - 从 zh/ 目录引用上级目录的资源
content = content.replace('href="index.html"', 'href="../index.html"')
content = content.replace('href="about.html"', 'href="about.html"')
content = content.replace('href="services.html"', 'href="services.html"')
content = content.replace('href="contact.html"', 'href="contact.html"')
content = content.replace('href="Logistics.html"', 'href="物流.html"')

# 修复语言切换链接
content = content.replace('href="../zh/world9h.com/index.html"', 'href="index.html"')
content = content.replace('href="../world9h.com/index.html"', 'href="../index.html"')

# 更新HTML语言属性
content = content.replace('lang="en"', 'lang="zh-CN"')

# 写入修复后的文件
with open('zh/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("中文首页修复完成！")
