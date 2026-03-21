import streamlit as st


# -------------------------- 全局页面配置 --------------------------
st.set_page_config(
    page_title="乡遇助梦·非遗文创甄选",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 初始化购物车会话状态 --------------------------
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 购物车操作函数（核心优化：移除st.rerun，改用st.toast轻提示）
def add_to_cart(product_name, price, quantity=1):
    for item in st.session_state.cart:
        if item["name"] == product_name:
            item["quantity"] += quantity
            st.toast(f"✅ {product_name} 数量+{quantity}，已加入购物车！", icon="🛒")
            return
    st.session_state.cart.append({
        "name": product_name,
        "price": price,
        "quantity": quantity
    })
    st.toast(f"✅ {product_name} 已加入购物车！", icon="🛒")

def remove_from_cart(product_name):
    st.session_state.cart = [item for item in st.session_state.cart if item["name"] != product_name]
    st.toast(f"❌ 已从购物车移除 {product_name}", icon="⚠️")

# -------------------------- 自定义CSS样式（优化DOM兼容性） --------------------------
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main {background-color: #FCFAF5; font-family: "Ma Shan Zheng", "PingFang SC", "Microsoft YaHei", sans-serif;}
    /* 关键：标题整体下移0.5cm（约3rem），并修复显示不全 */
    .block-container {
        padding-top: 3rem !important; 
        padding-bottom: 3rem !important; 
        max-width: 1400px !important; 
        margin: 0 auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* 艺术字主标题（完整显示+下移后位置） */
    .main-title {
        font-size: 52px !important; 
        color: #7A2C2C !important; 
        text-align: center !important; 
        font-weight: 700 !important;
        letter-spacing: 8px !important; 
        margin-bottom: 1.2rem !important;
        text-shadow: 2px 2px 4px rgba(122,44,44,0.15) !important;
        font-family: "Ma Shan Zheng", cursive !important;
        line-height: 1.2 !important;
        width: 100% !important;
        display: block !important;
    }
    /* 副标题艺术字 */
    .sub-title {
        font-size: 30px !important; 
        color: #9C3636 !important; 
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0 !important;
        border-left: 6px solid #C95A4A !important;
        padding-left: 14px !important;
        line-height: 1.3 !important;
        font-family: "Ma Shan Zheng", cursive !important;
        width: 100% !important;
    }
    /* 辅助文本 */
    .aux-text {
        text-align: center !important; 
        color: #886655 !important; 
        font-size: 18px !important;
        margin-bottom: 1.5rem !important; 
        letter-spacing: 2px !important;
    }
    /* 文创产品卡片 */
    .product-card {
        border: 1px solid #E8D7C6 !important; 
        border-radius: 16px !important;
        padding: 24px !important; 
        margin: 15px !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(122,44,44,0.06) !important;
        transition: all 0.3s ease !important;
    }
    .product-card:hover {
        box-shadow: 0 8px 24px rgba(122,44,44,0.12) !important;
        transform: translateY(-4px) !important;
    }
    /* 产品信息 */
    .product-name {
        font-size: 21px !important; 
        color: #332A25 !important; 
        font-weight: 600 !important;
        margin-bottom: 10px !important;
    }
    .product-price {
        font-size: 20px !important; 
        color: #D63031 !important; 
        font-weight: 700 !important;
        margin-bottom: 12px !important;
    }
    .product-desc {
        font-size: 15px !important; 
        color: #66554A !important; 
        line-height: 1.7 !important;
        text-align: justify !important;
    }
    /* 联系信息 */
    .contact-info {
        font-size: 17px !important; 
        color: #44332A !important; 
        line-height: 2.4 !important;
        margin-left: 8px !important;
    }
    /* 按钮样式 */
    .stButton>button {
        background-color: #7A2C2C !important; 
        color: white !important;
        border-radius: 10px !important; 
        border: none !important;
        padding: 8px 20px !important; 
        font-size: 16px !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #9C3636 !important;
    }
    /* 分割线 */
    hr {
        border-top: 1px solid #E8D7C6 !important;
        margin: 2rem 0 !important;
    }
    /* 页脚 */
    .footer {
        text-align: center !important; 
        color: #998877 !important; 
        font-size: 15px !important;
        margin-top: 3rem !important; 
        padding-top: 1.5rem !important;
        border-top: 1px solid #E8D7C6 !important;
    }
    /* 非遗介绍文本 */
    .fy-text {
        font-size: 16px !important; 
        color: #55443A !important; 
        line-height: 1.8 !important;
    }
    /* 侧边栏美化 */
    [data-testid="stSidebar"] {background-color: #F5F0EB !important;}
    /* 购物车样式 */
    .cart-item {
        padding: 10px !important;
        border-bottom: 1px dashed #E8D7C6 !important;
    }
    .cart-total {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #7A2C2C !important;
        margin-top: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------- 图片加载函数（核心优化：移除PIL依赖） --------------------------
def load_product_image(img_name):
    # 直接返回图片文件名（Streamlit会自动从仓库加载），失败时用网络占位图
    try:
        # 先尝试返回本地图片路径
        return img_name
    except:
        return "https://via.placeholder.com/400x300?text=乡遇助梦·非遗文创&font-size=16&color=7A2C2C&bgcolor=FCFAF5"

# -------------------------- 文创产品数据 --------------------------
XI_AN_WENCHUANG = [
    {
        "name": "亚克力立牌",
        "price": "¥18",
        "desc": "以“古今对话”为核心理念，将西安剪纸非遗技艺与唐代仕女形象相结合。设计采用异形轮廓，完全贴合剪纸图案的曲线与流动感，既保留传统剪纸“剪而不断”的工艺精髓，又通过亚克力材质的现代质感赋予其新颖的视觉表达。仕女衣袖与飞鸟的动态线条寓意着非遗技艺在当代的传承与新生，实现了从二维平面到三维立体的跨越，使非遗元素成为空间中独特的视觉焦点。",
        "img": "1.png"
    },
    {
        "name": "白鹿原非遗文化文创盲盒",
        "price": "¥108/套 | ¥27/只",
        "desc": "以白鹿原非遗文化（秦腔+泥叫叫）创新融合为设计基础，将陕西关中非遗技艺与《白鹿原》文化符号结合。含戏墩墩、皮啾啾、绒团团、秦盏盏四款，分别融入白鹿原古建筑、窑洞、戏楼等地域特色，泥叫叫为粘土烧制的民俗摆件（可吹响），秦腔元素则凸显关中戏曲文化，既是文创摆件也是民俗文化载体。",
        "img": "2.png"
    },
    {
        "name": "「长安十二时辰·非遗活态手账套装」",
        "price": "¥38",
        "desc": "以“西安非遗+古都时空叙事”为核心，聚焦年轻消费群体，将非遗转化为“可书写、可收藏、可体验”的日常文创。硬壳封面为西安剪纸浮雕工艺，内页按长安十二时辰划分章节，复刻凤翔木版年画唐代生活场景；配套剪纸书签、木版年画拓印工具包、农民画主题笔具，让千年非遗融入现代生活。",
        "img": "3.png"
    },
    {
        "name": "西安「唐宫乐舞」AR非遗折叠屏风",
        "price": "¥68",
        "desc": "提取西安皮影戏、西安鼓乐、唐三彩三大非遗元素，以唐代宫廷乐舞为核心场景打造3扇折叠迷你屏风。正面为皮影戏风格浮雕（复刻唐三彩釉色），背面印鼓乐古曲谱；扫描二维码/触碰NFC芯片可触发AR互动，浮雕人物随鼓乐起舞并同步展示非遗知识点，附赠mini皮影书签，兼具装饰与非遗科普价值。",
        "img": "4.png"
    },
    {
        "name": "「秦腔影韵」沉浸式皮影互动灯箱",
        "price": "¥68",
        "desc": "融合秦腔与华县皮影非遗文化，以“光影叙事”为核心打造可互动、可创作的体验产品。西安古城墙砖石纹理实木框架，正面高透亚克力板，背面磁吸接口可自由更换多层镂空皮影片（以《三滴血》《火焰驹》为原型）；配备投影镜头与秦腔音效，可调节灯光、切换唱腔，附赠空白皮影坯料与雕刻工具，实现非遗体验+创作双重价值。",
        "img": "5.png"
    },
    {
        "name": "「长安百味·食光盲盒」",
        "price": "¥38/个",
        "desc": "以西安传统美食文化为载体，融合兵马俑、唐侍女、大雁塔等陕西历史意象做拟人化设计，AIGC生成角色与背景故事。首弹含6款常规款（肉夹馍·秦武士、凉皮·唐舞姬等）+1款隐藏款（长安宴·帝王套组），扫描AR码可观看美食起源动画或非遗制作过程，收藏与趣味性兼具。",
        "img": "6.png"
    },
    {
        "name": "西安非遗剪纸旋转收纳笔筒",
        "price": "¥38",
        "desc": "以西安剪纸为核心非遗载体，融合月牙纹、锯齿纹技法与柿蒂纹、石榴纹吉祥元素。采用三层360°旋转结构，磁吸式顶盖可作杯垫，胡桃木配重底座稳固防倾倒；外侧激光雕刻大雁塔+地铁、石榴缠枝纹等剪纸图案，填涂朱砂红呼应剪纸本色，兼具办公实用属性与商务礼品价值，让非遗融入日常办公。",
        "img": "7.png"
    },
    {
        "name": "华县皮影+西安地标 模块化手机支架",
        "price": "¥18",
        "desc": "磁吸式底座搭配可替换皮影插片，插片融合华县皮影人物与大雁塔、古城墙等西安地标，手工组装无难度。解决传统地标文创单一问题，兼具手机支架的实用功能与皮影装饰效果，互动性强，是高性价比的非遗文创小物。",
        "img": "8.png"
    }
]

AN_KANG_WENCHUANG = [
    {
        "name": "彩莲船立体贺卡",
        "price": "¥18",
        "desc": "以安康彩莲船非遗为灵感，将传统舞蹈元素融入立体贺卡设计。船体造型还原彩莲船轻盈灵动的特点，色彩选用非遗传统配色，立体结构象征彩莲船在水面的动态美感。打开贺卡仿佛一艘彩莲船从汉江驶来，既保留非遗文化视觉符号，又赋予现代实用功能，传递祝福的同时感受陕南非遗魅力。",
        "img": "9.png"
    },
    {
        "name": "「汉水三声· 非遗雅集套装」",
        "price": "¥98/套",
        "desc": "融合汉水陶、旬阳木刻版画、汉黄二调三大安康非遗，打造“可听、可赏、可用、可藏”的沉浸式文创。含汉水陶手工茶壶+品茗杯、木刻版画主题手账本、汉水陶香插、唱词书签套装；壶盖扫码可收听汉黄二调经典选段，器物表面印制旬阳木刻版画经典纹样，全方位传递秦巴汉水的文化底蕴。",
        "img": "10.png"
    },
    {
        "name": "安康「秦巴福韵」非遗互动香包灯",
        "price": "¥8",
        "desc": "融合安康汉阴剪纸与紫阳毛尖茶文化，打造“视觉+嗅觉+触觉”三重体验的文创。打破传统香包单一佩戴属性，内置可充电LED柔光灯，双层设计：外层柞蚕丝面料手工拓印汉阴剪纸镂空纹样（透光成影），内层可替换紫阳毛尖+艾草混合香包芯；竹制灯座搭配磁吸充电，兼具香薰、小夜灯、装饰功能，适配多场景使用。",
        "img": "11.png"
    },
    {
        "name": "「汉调二黄·戏梦人生」BJD可换装玩偶",
        "price": "¥108/只",
        "desc": "以国家级非遗汉调二黄为核心，提取《宇宙锋》《二进宫》经典剧目的角色形象、戏服纹样、脸谱妆容设计。AIGC生成虚拟角色原型与服饰纹样，支持VR/AR预览换装效果；每套戏服配套NFT数字身份卡，扫描可观看对应剧目的AI生成微短剧片段，收藏价值高。",
        "img": "12.png"
    },
    {
        "name": "安康元素马克杯",
        "price": "¥28",
        "desc": "杯身保留陶土自然颗粒感，触感温润，杯口微弧处理贴合唇形，避免刮擦。黑、米白、红三色设计显现代简约感，杯身印制旬阳木刻版画元素的安康特色梯田图案，将陕南非遗与日常饮水器具结合，兼具实用性与文化展示价值。",
        "img": "13.png"
    },
    {
        "name": "木刻版画「镂空透光」耳机壳",
        "price": "¥38",
        "desc": "硬壳表面雕刻安康木刻版画非遗纹样，纹样选取民俗场景、汉水风光等特色元素，镂空处贴透光膜，耳机亮灯时纹样可透出微光，增加使用趣味性。背面可贴个性化贴纸，既体现陕南非遗工艺，又满足年轻人的个性化、潮流化需求，非遗与现代潮品完美融合。",
        "img": "14.png"
    }
]

# -------------------------- 侧边栏导航（购物车入口） --------------------------
st.sidebar.header("🏮 乡遇助梦·非遗文创甄选")
st.sidebar.divider()

# 购物车侧边栏展示（优化：移除删除按钮的st.rerun）
with st.sidebar.expander("🛒 我的购物车", expanded=False):
    if st.session_state.cart:
        total_price = 0
        for idx, item in enumerate(st.session_state.cart):
            price_str = item["price"].split("|")[0].replace("¥", "").replace("/套", "").replace("/个", "").replace("/只", "")
            price = float(price_str)
            item_total = price * item["quantity"]
            total_price += item_total
            
            st.markdown(f'<div class="cart-item">', unsafe_allow_html=True)
            col_cart1, col_cart2, col_cart3, col_cart4 = st.columns([3,1,1,1])
            with col_cart1:
                st.write(f"📌 {item['name']}")
            with col_cart2:
                st.write(f"¥{price}")
            with col_cart3:
                st.write(f"×{item['quantity']}")
            with col_cart4:
                if st.button("🗑️", key=f"del_{idx}"):
                    remove_from_cart(item["name"])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<p class="cart-total">合计：¥{total_price:.2f}</p>', unsafe_allow_html=True)
        if st.button("清空购物车", key="clear_cart"):
            st.session_state.cart = []
            st.toast("🛒 购物车已清空！", icon="✅")
    else:
        st.write("购物车空空如也～快去挑选心仪的文创吧✨")

page = st.sidebar.radio(
    "🔍 导航菜单",
    ["首页·非遗文化介绍", "西安非遗文创甄选", "安康非遗文创甄选", "售后保障·联系我们"],
    index=0,
    help="点击切换页面，查看文创详情与售后信息"
)
st.sidebar.divider()
st.sidebar.info("✨ 以文创为媒，助力非遗活态传承；以乡遇为桥，赋能乡村文化振兴～")

# -------------------------- 页面1：首页 --------------------------
if page == "首页·非遗文化介绍":
    st.markdown('<p class="main-title">乡遇助梦·非遗文创甄选</p>', unsafe_allow_html=True)
    st.markdown('<p class="aux-text">非遗焕新 · 乡创赋能 · 文化传承</p>', unsafe_allow_html=True)
    st.divider()

    col_xa, col_ak = st.columns(2, gap="large")
    with col_xa:
        st.markdown('<p class="sub-title">西安非遗 · 十三朝古都的文化底蕴</p>', unsafe_allow_html=True)
        st.image(load_product_image("首页1.png"), use_container_width=True, caption="西安非遗：剪纸/皮影/秦腔/鼓乐")
        st.markdown('<p class="fy-text">西安作为十三朝古都，非遗文化历经千年沉淀，剪纸、华县皮影、秦腔、西安鼓乐、凤翔木版年画等技艺熠熠生辉。本次西安文创以「古今对话」为核心理念，将传统非遗技艺与现代设计、AR/NFC等科技深度融合，打破非遗的展示边界，让千年古都的文化记忆从展厅走向日常，实现「可看、可触、可体验、可收藏」的全新表达，让非遗在当代焕发出新的生命力。</p>', unsafe_allow_html=True)

    with col_ak:
        st.markdown('<p class="sub-title">安康非遗 · 秦巴汉水的民俗风情</p>', unsafe_allow_html=True)
        st.image(load_product_image("首页2.png"), use_container_width=True, caption="安康非遗：彩莲船/汉调二黄/木刻版画/汉水陶")
        st.markdown('<p class="fy-text">安康地处秦巴汉水之间，陕南非遗兼具鲜明的地域特色与温润的民俗温度，彩莲船、汉调二黄、旬阳木刻版画、汉水陶等技艺代代相传。本次安康文创以「秦巴福韵·汉水之声」为核心，融合茶文化、戏曲文化、陶艺文化，打造「视觉+听觉+嗅觉」的沉浸式体验，让陕南非遗融入办公、居家、赠礼等日常场景，以文创为载体助力乡村文化振兴，让秦巴汉水的文化魅力被更多人看见。</p>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<p class="sub-title" style="text-align:center;">核心理念 · 乡遇助梦</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown('<p style="text-align:center; font-size:19px; font-weight:600; color:#7A2C2C;">非遗焕新</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#66554A;">传统非遗技艺与现代设计结合，让老手艺焕发新活力</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p style="text-align:center; font-size:19px; font-weight:600; color:#7A2C2C;">乡创赋能</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#66554A;">以文创为载体，助力乡村非遗产业发展，带动乡创增收</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p style="text-align:center; font-size:19px; font-weight:600; color:#7A2C2C;">文化传承</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#66554A;">让非遗文化走进大众生活，实现活态传承与世代延续</p>', unsafe_allow_html=True)

# -------------------------- 页面2：西安文创（购物车按钮） --------------------------
elif page == "西安非遗文创甄选":
    st.markdown('<p class="main-title">西安非遗文创甄选</p>', unsafe_allow_html=True)
    st.markdown('<p class="aux-text">古都非遗 · 焕新呈现 </p>', unsafe_allow_html=True)
    st.divider()

    for idx, product in enumerate(XI_AN_WENCHUANG):
        if idx % 2 == 0:
            col1, col2 = st.columns(2, gap="medium")
        current_col = col1 if idx % 2 == 0 else col2

        with current_col:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            st.image(load_product_image(product["img"]), use_container_width=True, caption=product["name"])
            st.markdown(f'<p class="product-name">{product["name"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-price">售价：{product["price"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-desc">{product["desc"]}</p>', unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 2])
            with col_btn1:
                quantity = st.number_input("数量", min_value=1, max_value=10, value=1, key=f"qty_xa_{idx}", label_visibility="collapsed")
            with col_btn2:
                if st.button(f"加入购物车", key=f"add_xa_{idx}", use_container_width=True):
                    add_to_cart(product["name"], product["price"], quantity)
            
            st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 页面3：安康文创（购物车按钮） --------------------------
elif page == "安康非遗文创甄选":
    st.markdown('<p class="main-title">安康非遗文创甄选</p>', unsafe_allow_html=True)
    st.markdown('<p class="aux-text">秦巴汉水 · 乡创之美 </p>', unsafe_allow_html=True)
    st.divider()

    for idx, product in enumerate(AN_KANG_WENCHUANG):
        if idx % 2 == 0:
            col1, col2 = st.columns(2, gap="medium")
        current_col = col1 if idx % 2 == 0 else col2

        with current_col:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            st.image(load_product_image(product["img"]), use_container_width=True, caption=product["name"])
            st.markdown(f'<p class="product-name">{product["name"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-price">售价：{product["price"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-desc">{product["desc"]}</p>', unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 2])
            with col_btn1:
                quantity = st.number_input("数量", min_value=1, max_value=10, value=1, key=f"qty_ak_{idx}", label_visibility="collapsed")
            with col_btn2:
                if st.button(f"加入购物车", key=f"add_ak_{idx}", use_container_width=True):
                    add_to_cart(product["name"], product["price"], quantity)
            
            st.markdown('</div>', unsafe_allow_html=True)

# -------------------------- 页面4：售后 --------------------------
elif page == "售后保障·联系我们":
    st.markdown('<p class="main-title">售后保障 · 联系我们</p>', unsafe_allow_html=True)
    st.divider()

    st.warning("📦 售后保障规则：① 所有文创支持7天无理由退换（未拆封、无破损、不影响二次销售）；② 定制款文创不支持无理由退换；③ 非遗文创多为手工/半手工制作，轻微工艺差异不影响使用均属正常，非质量问题。")
    st.divider()

    col_contact, col_leavemsg = st.columns([1, 2], gap="large")
    with col_contact:
        st.markdown('<p class="sub-title">📞 官方联系方式</p>', unsafe_allow_html=True)
        st.markdown("""
            <div class="contact-info">
            📱 文创咨询/订购：138 0000 1234<br>
            📧 售后邮箱：xiangyuzhumeng@163.com<br>
            🛰️ 微信客服：XiangYuZhuMeng-WC（乡遇助梦文创）<br>
            📍 线下体验点：陕西省西安市碑林区非遗文创街区<br>
            ⏰ 服务时间：9:00-21:00（全年无休）<br>
            🚚 物流说明：满58元包邮，陕西境内次日达，全国3-5日达
            </div>
        """, unsafe_allow_html=True)
        st.image(load_product_image("ewm.png"), use_container_width=False, width=220, caption="扫码添加微信客服，享专属优惠")

    with col_leavemsg:
        st.markdown('<p class="sub-title">✍️ 在线留言反馈</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#66554A; font-size:15px;">带<span style="color:#D63031;">*</span>为必填项，客服将在1小时内与您联系</p>', unsafe_allow_html=True)
        with st.form(key="leave_msg_form", clear_on_submit=True):
            name = st.text_input("您的姓名", placeholder="请输入姓名/昵称", key="name_input")
            phone = st.text_input("联系方式", placeholder="手机号/微信号", key="phone_input")
            problem_type = st.selectbox("问题类型", ["产品咨询", "订购下单", "售后退换", "定制需求", "其他问题"])
            problem = st.text_area("问题详细描述", placeholder="请说明您的问题/需求，如产品规格、物流问题等", 
                                   height=180, key="problem_input")
            submit_btn = st.form_submit_button("提交留言", use_container_width=True)

            if submit_btn:
                if not name.strip():
                    st.toast("❌ 请填写您的姓名！", icon="⚠️")
                elif not phone.strip():
                    st.toast("❌ 请填写有效的联系方式！", icon="⚠️")
                elif not problem.strip():
                    st.toast("❌ 请详细描述您的问题/需求！", icon="⚠️")
                else:
                    st.toast("✅ 留言提交成功！客服将在1小时内与您联系，感谢信任～", icon="✅")

    st.markdown('<p class="footer">© 2025 乡遇助梦·非遗文创甄选 版权所有 | 助力非遗传承 · 赋能乡村文创</p>', unsafe_allow_html=True)
