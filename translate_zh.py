import os
import re

# Target directory
target_dir = r'd:\Project\world9h.com\world9h-website\zh'

# Translations dictionary
# Keys are regex patterns, Values are replacement strings
translations = {
    # --- Navigation & Common Elements ---
    r'>\s*HOME\s*<': '>首页<',
    r'>\s*Home\s*<': '>首页<',
    r'>\s*ABOUT US\s*<': '>关于我们<',
    r'>\s*About Us\s*<': '>关于我们<',
    r'>\s*SERVICE\s*<': '>业务范围<',
    r'>\s*SERVICES\s*<': '>业务范围<',
    r'>\s*Services\s*<': '>业务范围<', # Case variation
    r'>\s*Services:\s*<': '>业务范围:<', # With colon
    r'>\s*CONTACT US\s*<': '>联系我们<',
    r'>\s*Contact Us\s*<': '>联系我们<',
    r'>\s*NEWS\s*<': '>新闻中心<',
    r'>\s*News\s*<': '>新闻中心<',
    r'>\s*INDEX\s*<': '>首页<',
    r'>\s*LATEST NEWS\s*<': '>最新新闻<',
    r'>\s*Latest News\s*<': '>最新新闻<',
    r'>\s*Real-time news\s*<': '>实时新闻<',
    r'>\s*Subscribe\s*<': '>订阅<',
    
    # --- Company Name ---
    # Handles multi-line or single-line variations
    r'>\s*THE NINE INTERNATIONAL SUPPLY\s+CHAIN\s*<': '>九鸿国际供应链管理有限公司<',
    r'The Nine International Supply Chain': '九鸿国际供应链管理有限公司',
    r'>\s*The Nine H: International Tamrading\s*<': '>九鸿国际: 国际贸易<',
    
    # --- Slogans & Hero Text ---
    r'>\s*Unlocking Opportunities in the Global Marketplace\s*<': '>开启全球市场新机遇<',
    r'>\s*Efficiency, Integrity, and Prosperity in Trade\s*<': '>效率、诚信、共赢<',
    r'>\s*The latest commodity trade service news, learn more about us\.\s*<': '>最新的大宗商品贸易服务资讯，了解更多。<',
    r'>\s*The latest logistics service news, learn more about us\.\s*<': '>最新的物流服务资讯，了解更多。<',
    r'>\s*YOU CAN TRUST US\s*<': '>值得您的信赖<',
    r'>\s*What makes you choose us and trust us\?\s*': '>为什么选择我们要信任我们？',
    
    # --- Contact Form ---
    r'placeholder="Enter your name"': 'placeholder="请输入您的姓名"',
    r'placeholder="Enter your phone number"': 'placeholder="请输入您的电话号码"',
    r'placeholder="Enter your email"': 'placeholder="请输入您的邮箱"',
    r'placeholder="Enter your question"': 'placeholder="请输入您的问题"',
    r'>\s*Submit\s*<': '>提交<',
    r'>\s*Your profile and questions\s*<': '>您的资料与问题<',
    
    # --- Service Categories & Lists ---
    r'>\s*Logistics\s*<': '>物流<',
    r'>\s*Commodity Trade\s*<': '>大宗商品贸易<',
    r'>\s*International Letter of Credit\s*<': '>国际信用证<',
    r'>\s*Standby Letter of Credit\s*<': '>备用信用证<',
    r'>\s*Reliable Sourcing\s*<': '>可靠的采购<',
    r'>\s*Efficient Logistics\s*<': '>高效的物流<',
    r'>\s*Secure Transactions\s*<': '>安全的交易<',
    r'>\s*Customer-centric Approach\s*<': '>以客户为中心的方法<',
    r'>\s*Compliance and Integrity\s*<': '>合规与诚信<',
    r'>\s*Extensive Global Network\s*<': '>广泛的全球网络<',
    r'>\s*Expertise in Market Analysis\s*<': '>市场分析专长<',
    r'>\s*Robust Quality Control\s*<': '>严格的质量控制<',
    r'>\s*Risk Mitigation and Compliance\s*<': '>风险缓解与合规<',
    r'>\s*Comprehensive Service Offering\s*<': '>全面的服务提供<',
    r'>\s*Consultation and Advising\s*<': '>咨询与建议<',
    r'>\s*Application and Documentation\s*<': '>申请与文件<',
    r'>\s*Issuance and Confirmation\s*<': '>签发与确认<',
    r'>\s*Compliance Checks\s*<': '>合规检查<',
    r'>\s*Negotiation and Amendments\s*<': '>谈判与修订<',
    r'>\s*Presentation and Examination\s*<': '>提交与审查<',
    r'>\s*Payment and Settlement\s*<': '>付款与结算<',
    r'>\s*Discrepancy Resolution\s*<': '>不符点解决<',

    # --- Long Text Paragraphs (Using partial match keywords or unique beginnings relative to tags if simpler, but regex usually best) ---
    
    # About Us - Intro
    r'>\s*Some introductions about our company let you know us better\s*<': '>关于我们公司的简介，让您更了解我们<',
    
    # About Us - Reliable Sourcing Body
    r'At The Nine International Supply Chain, we offer reliable sourcing and efficient logistics services.*?ethical practices\.': 
    '在九鸿国际供应链，我们提供可靠的采购和高效的物流服务，以确保贸易交易的无缝和安全。我们以客户为中心，优先考虑合规和诚信，严格遵守国际贸易法规和道德规范。',
    
    # About Us - Expertise Body
    r'Our expertise lies in providing trusted procurement channels.*?operational efficiency\.':
    '我们的专长在于提供值得信赖的大宗商品采购渠道，保证始终如一的质量和可靠的货源。通过简化供应链和优化物流，我们确保及时交付并最大化运营效率。',
    
    # About Us - Customer Focus Body
    r'With a focus on customer satisfaction, we prioritize building long-term partnerships.*?risk-mitigated transactions\.':
    '我们注重客户满意度，致力于建立基于信任和透明度的长期合作伙伴关系。我们对合规和诚信的承诺确保客户能够进行安全且风险可控的交易。',

    # About Us - Conclusion Body
    r'Choose The Nine International Supply Chain for our industry expertise.*?utmost professionalism\.':
    '选择九鸿国际供应链，因为我们拥有行业专长、具有竞争力的价格以及满足您独特需求的定制解决方案。我们是您值得信赖的合作伙伴，助您应对国际贸易的复杂性，以最专业的精神提供可靠的采购、高效的物流和安全的交易。',
    
    # Services - Intro
    r'At The Nine International Supply Chain, our commitment to efficiency, integrity, and prosperity.*?global marketplace\.':
    '在九鸿国际供应链，我们对效率、诚信和繁荣的承诺推动着我们全面的大宗商品贸易服务。我们优先简化供应链，确保交易透明，并培养互利关系，以在全球市场上取得客户的成功。',
    
    # Services - ILC Body
    r'Our international letter of credit \(ILC\) service ensures secure and efficient trade transactions.*?mitigating risks':
    '我们的国际信用证 (ILC) 服务确保贸易交易的安全和高效。我们协助客户处理复杂的信用证开立流程，包括文件准备、合规性检查和与银行的协调，以促进顺畅可靠的交易，同时降低风险',
    
    # Contact - Intro
    r'Thank you for your interest in our services\. We are eager to assist you.*?global trade endeavors\.':
    '感谢您对我们的服务感兴趣。我们渴望协助您满足国际大宗商品贸易需求。无论您需要可靠的采购、高效的物流、专业的市场洞察、国际信用证服务，还是包含各个方面的综合解决方案，我们的专业团队都准备好提供量身定制的解决方案，以推动您的成功。立即联系我们，探讨我们要如何合作，释放您全球贸易事业的全部潜力。',

    # --- News Headlines (Logistics.html) ---
    r'US escalates Mexico corn trade spat with dispute panel request': '美国因转基因玉米贸易争端升级要求成立争端解决小组',
    r"Brazil's JBS remains optimistic on China despite short-term woes": '尽管短期困难，巴西JBS对中国市场仍保持乐观',
    r'Rice export ban:Why India is so crucial to global rice trade': '大米出口禁令：为什么印度对全球大米贸易至关重要',
    r'Grain futures calm down but Russia-Ukraine supplies more precarious than ever': '谷物期货平稳，但俄乌供应比以往任何时候都更不稳定',
    r'Shanghai Clearing House launches digital yuan services for commodity trading': '上海清算所推出数字人民币大宗商品交易服务',
    
    # News Descriptions (Summaries)
    r'The United States on Thursday escalated its objections to Mexico\'s curbs on genetically modified corn imports.*?': 
    '美国周四升级了对墨西哥限制转基因玉米进口的反对，根据北美贸易协定要求成立争端解决小组...',
    
    r'Speaking at an industry event on Thursday, JBS CEO Gilberto Tomazoni said he still believes.*?':
    'JBS首席执行官Gilberto Tomazoni在周四的一次行业活动中表示，他仍然相信中国的牛肉消费量将随着时间的推移而增加...',
    
    r'India accounts for more than 40% of global rice exports.*?':
    '印度占全球大米出口的40%以上...',
    
    r'Wheat futures on the Chicago Board of Trade swung between losses and gains.*?':
    '芝加哥期货交易所的小麦期货在涨跌之间波动...',
    
    r'The services allow users to make cross-bank clearings and settlements.*?':
    '该服务允许用户使用数字人民币进行大宗商品的跨行清算和结算...',
    
    # List item details
    r'Extensive Global Network': '广泛的全球网络', 
    r'Our company boasts an extensive global network of trusted suppliers, buyers, and shipping partners.*?reliable trade transactions\.':
    '我们公司拥有由值得信赖的供应商、买家和运输合作伙伴组成的广泛全球网络，使我们需要能够获得各种高质量的大宗商品，并确保高效可靠的贸易交易。',
    
    r'Expertise in Market Analysis': '市场分析专长',
    r'Our team of seasoned professionals possesses in-depth knowledge and expertise in market analysis.*?informed decisions\.':
    '我们经验丰富的专业团队在市场分析方面拥有深入的知识和专业技能，能够为客户提供有价值的见解和指导。我们时刻关注市场趋势、供需动态和监管变化，帮助客户做出明智的决策。',
    
    r'Robust Quality Control': '严格的质量控制',
    r'We have stringent quality control procedures in place to ensure that the commodities.*?deliver to our clients\.':
    '我们要建立了严格的质量控制程序，以确保我们采购和交易的大宗商品符合最高标准。我们严格的检验和测试流程保证了我们向客户交付的产品始终如一的质量。',
    
    r'Risk Mitigation and Compliance': '风险缓解与合规',
    r'We prioritize risk mitigation and compliance with international trade regulations.*?minimizing risks for our clients\.':
    '我们优先考虑风险缓解并遵守国际贸易法规。我们在管理国际信用证和处理复杂的贸易单证方面的专业知识确保了交易的安全和合规，最大限度地降低了客户的风险。',
    
    r'Customer-centric Approach': '以客户为中心的方法',
    r'We prioritize customer satisfaction and strive to build long-term partnerships.*?meet their specific needs\.':
    '我们优先考虑客户满意度，并致力于建立基于信任、透明和共同成长的长期合作伙伴关系。我们敬业的团队提供个性化的关注，理解每位客户的独特需求，并提供量身定制的解决方案。',
    
    r'Comprehensive Service Offering': '全面的服务提供',
    r'We provide a comprehensive range of services, including reliable sourcing.*?trading needs\.':
    '我们提供全面的服务，包括可靠的采购、高效的物流、专业的市场洞察和国际信用证服务。我们的综合方法确保客户拥有一站式解决方案，满足其国际大宗商品贸易需求。',
    
    # Misc
    r'>\s*01\s*<': '>01<',
    # --- Complex Body Paragraphs (containing HTML entities for the company name) ---
    # We use a regex helper for the company name entity sequence if needed, but here we paste the exact strings found.
    # formatting: '&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;'
    
    # about.html
    r'At\s+&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;,\s+we\s+offer\s+reliable\s+sourcing\s+and\s+efficient\s+logistics\s+services.*?\ ethical\s+practices\.':
    '在九鸿国际供应链管理有限公司，我们提供可靠的采购和高效的物流服务，以确保无缝和安全的贸易交易。本着以客户为中心的方法，我们优先考虑合规性和诚信，严格遵守国际贸易法规 and 道德规范。',
    
    r'Choose\s+&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;\s+for\s+our\s+industry\s+expertise.*?\ utmost\s+professionalism\.':
    '选择九鸿国际供应链管理有限公司，因为我们拥有行业专长、极具竞争力的价格以及满足您独特需求的定制解决方案。我们是您在复杂的国际贸易中值得信赖的合作伙伴，以极其专业的精神提供可靠的采购、高效的物流和安全的交易。',

    # services.html
    r'At\s+&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;,\s+our\s+commitment\s+to\s+efficiency.*?\ global\s+marketplace\.':
    '在九鸿国际供应链管理有限公司，我们对效率、诚信和繁荣的承诺推动着我们全面的商品贸易服务。我们优先优化供应链，确保交易透明，并建立互惠互利的关系，助力客户在全球市场中取得成功。',
    
    # index.html (Homepage)
    r'Experience\s+the\s+unrivaled\s+excellence\s+of\s+&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;.*?trade\s+facilitation\.':
    '体验九鸿国际供应链管理有限公司无与伦比的卓越服务。我们为全球大宗商品贸易、国际信用证和备用信用证提供一流的解决方案，为您的业务提供最大的便利、安全和盈利能力。我们尖端的服务确保无缝交易、风险缓解和无与伦比的贸易便利化。',

    r'At\s+&#39321;&#28207;&#20061;&#40511;&#20379;&#24212;&#38142;&#31649;&#29702;&#26377;&#38480;&#20844;&#21496;,\s+we\s+excel\s+in\s+international\s+commodity\s+trading.*?\ global\s+trade\.':
    '在九鸿国际供应链管理有限公司，我们擅长国际大宗商品贸易，采购高质量材料并提供跨行业的无缝解决方案，包括铁矿石、煤炭、农产品和海运。相信我们是您值得信赖的合作伙伴，释放全球贸易的潜力。',

    r'We\s+specialize\s+in\s+international\s+letter\s+of\s+credit\s+services.*?\ with\s+expertise\.':
    '我们专注于国际信用证服务，通过管理开立和管理信用证的复杂性，以专业的知识驾驭国际贸易法规，确保安全高效的贸易交易。',

    r'>\s*Provide\s+professional\s+commodity\s+trading\s+services\s+for\s+our\s+customers\.\s*<': '>为我们的客户提供专业的大宗商品贸易服务。<',
    
    r'>\s*Connecting\s+Markets,\s+Empowering\s+Trade\s*<': '>连接市场，赋能贸易<',
    
    r'>\s*Customs\s+and\s+customer\s+satisfaction\s*<': '>海关与客户满意度<',
    r'>\s*Logistics\s+of\s+transactions\s*<': '>交易物流<',
    r'>\s*Fast\s+customs\s+clearance\s*<': '>快速通关<',
    r'>\s*LEARN\s+MORE\s*<': '>了解更多<',
    
    # Fixes
    r'>\s*业务体系\s*<': '>业务范围<',
    r'&#19994;&#21151;&#20307;&#31995;': '业务范围', # Fix for "Ye Gong Ti Xi" entity encoding typo

    r'>\s*03\s*<': '>03<',
    r'>\s*04\s*<': '>04<',
    r'>\s*05\s*<': '>05<',
    r'>\s*06\s*<': '>06<',

    # Mixed Content Fixes (about.html / services.html)
    r'Our company boasts an 广泛的全球网络 of trusted suppliers, buyers, and shipping partners, enabling us to access a wide range of high-quality commodities and ensure efficient and reliable trade transactions\.':
    '我们公司拥有广泛的全球网络，涵盖值得信赖的供应商、买家和航运合作伙伴，使我们能够获取各种优质大宗商品，并确保高效可靠的贸易交易。',

    r'Our team of seasoned professionals possesses in-depth knowledge and 市场分析专长, enabling us to provide valuable insights and guidance to our clients\.':
    '我们的资深专业团队拥有深厚的知识和市场分析专长，使我们能够为客户提供有价值的见解和指导。我们时刻关注市场趋势、供需动态和监管变化，帮助客户做出明智的决策。',
    
    # "Prominent Player" paragraph
    r'At (?:The Nine H|九鸿国际供应链管理有限公司|The Nine International\s+Supply Chain|The Nine H International Trading Pte\. Ltd\.|九鸿国际供应链管理有限公司 Management Group Holdings Limited\.)[,\s]*we are a prominent player in international commodity trading, offering comprehensive services across various sectors\. With expertise in iron ore, coal, agricultural commodities, and maritime shipping, we provide seamless and professional solutions to meet our clients\' diverse needs\.': '九鸿国际供应链管理有限公司是大宗商品国际贸易领域的知名企业，在各个领域提供全面的服务。凭借在铁矿石、煤炭、农产品和海运方面的专业知识，我们提供无缝且专业的解决方案，以满足客户的多样化需求。',



    # Fix: "business@theworld9h.com" -> "business@world9h.com" in other places (like footer list)
    r'business@theworld9h\.com': 'business@world9h.com',


    # "Prominent Player" paragraph - Retaining this, assuming it might work or needs the HTML tags
    r'At (?:The Nine H|九鸿国际供应链管理有限公司).*?prominent player.*?diverse needs\.': '九鸿国际供应链管理有限公司是大宗商品国际贸易领域的知名企业，在各个领域提供全面的服务。凭借在铁矿石、煤炭、农产品和海运方面的专业知识，我们提供无缝且专业的解决方案，以满足客户的多样化需求。',


    # Typo fix: "业功" (Ye Gong) -> "业务" (Ye Wu)
    r'&#19994;&#21151;': '业务', # Fixes 业功 -> 业务

    r'We prioritize 风险缓解与合规 with international trade regulations\. Our expertise in managing international letters of credit and navigating complex trade documentation ensures secure and compliant transactions, minimizing risks for our clients\.':
    '我们优先考虑风险缓解与合规，严格遵守国际贸易法规。我们在管理国际信用证和处理复杂贸易单证方面的专长，确保了交易的安全和合规，最大限度地为客户降低风险。',

    # General replacements (broad)
    r'业务体系[:：]?': '业务范围',
}

def clean_text(text):
    # Helper to check if translation exists (optional logging)
    return text

def translate_files():
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                print(f"Processing {path}...")
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                for pattern, replacement in translations.items():
                    # Sanitize replacement pattern for re.sub if it contains backreferences (it shouldn't here but good practice)
                    # We are doing literal string replacement generally, but using regex for matching.
                    try:
                        # Use re.sub. We use re.DOTALL if we want . to match newlines, but we want \s+ to match newlines
                        # Generally our patterns don't use . much, except for the long text logic above.
                        # For the long texts, I used .*? which implies regex mode.
                        # So I must ensure special regex chars in the KEYS are escaped if they are literal.
                        # Wait! I put regex characters like .*? in the keys above.
                        # BUT I also have literal strings like "At The Nine...".
                        # Literal strings in regex need escaping if they contain ()[]{} etc.
                        # I should probably manually ensure my huge keys are safe or regex-ready.
                        # Most of my keys are safe text + whitespace \s.
                        # "International Letter of Credit (ILC)" contains parens!
                        # I need to escape parens in the keys if they are part of the text.
                        # I'll let the user run this script and see if it fails, or I should fix it now?
                        # I'll fix the known parens.
                        
                        new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE|re.DOTALL)
                    except Exception as e:
                        print(f"Error on pattern: {pattern[:20]}... : {e}")
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Translated {file}')
                    count += 1
                else:
                    print(f'No changes for {file}')

    print(f"Total files updated: {count}")

if __name__ == '__main__':
    translate_files()
