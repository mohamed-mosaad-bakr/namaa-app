# نماء — دليل التسليم (لأي شات أو مطوّر جديد)

اقرا الملف ده و`CLAUDE.md` قبل أي تعديل. الاتنين مع بعض كفاية تكمّل من غير ما حد يشرحلك حاجة.

## التطبيق في سطرين
نماء تطبيق عربي (RTL، عامية مصرية) لمتابعة صافي الثروة والدخل السلبي والميزانية والديون، والهدف الأساسي: ياخد بإيد المستخدم من أي مرحلة (مديون ← بيصرف كل اللي بييجي ← بيحوّش ← بيستثمر) لحد الحرية المالية.
بيشتغل كموقع (PWA من الريبو ده) وكتطبيق أندرويد (APK = WebView بيحمّل نفس `index.html`).

## الملفات
| الملف | دوره |
|---|---|
| `index.html` | التطبيق كله في ملف واحد: React متصغّر + موديولات DOM |
| `version.json` | `build` و`version` و`notes`. الـ APK بيقراه أول ما يفتح، ولو الـ build أعلى بيعرض «حدّث دلوقتي» |
| `manifest.webmanifest`, `sw.js`, `icon-*.png` | إعدادات الـ PWA (شاشة الفتح خضرا `#1F5C40`) |
| `namaa-26.3.apk` | آخر APK (أيقونة بتتغيّر مع لون التطبيق) |
| `tools/release.py` | بيرفع رقم الإصدار ويفحص الكود قبل النشر |
| `CLAUDE.md` | قواعد النشر الإلزامية |

## شكل الكود جوه `index.html`
1. **سكريبت React الرئيسي** (اللي فيه `InvestmentCalculator`): الصفحات الأساسية (الرئيسية، الأصول، الدخل، التحليل، الإعدادات، محرّر الأصل). متصغّر، فالتعديل بيكون بالبحث عن نص فريد واستبداله (Python `str.replace` مع `assert count==1`).
2. **موديولات DOM** بعده، كل واحد في `<script>` بيبدأ بتعليق `/* NAMAA_<الاسم> vN — شرح */`. أهمها:
   - `NAMAA_SYNC` مزامنة Firebase (REST) مع **تشفير كامل على الجهاز** (AES-GCM، المفتاح من باسورد الحساب بـ PBKDF2). لو الباسورد اتنسي، النسخة اللي على السحابة مش بترجع.
   - `NAMAA_BUDGET` ميزانيتي (دخل، مصاريف، ديون بأقساط وسجل دفعات، سلف). `NAMAA_PLAN` خطتي. `NAMAA_LEARN` تعلّم (مكتبة يوتيوب + ترشيح حسب حالة المستخدم). `NAMAA_DEEN` نعمة اليوم. `NAMAA_ZAKAT` الزكاة.
   - `NAMAA_TRADE` شراء أسهم (بحث بالرمز أو الاسم من TradingView). `NAMAA_TRANSFER` تحويل بين الأصول (وحسابات التداول عن طريق «رصيد كاش»).
   - `NAMAA_ONBOARD` البداية (5 صفحات بالسحب + أسئلة). `NAMAA_TABS` الشريط اللي تحت (قابل للتخصيص). `NAMAA_SETORG` ترتيب الإعدادات.
   - `NAMAA_SNACK` الرسالة الصغيرة تحت + «تراجع». `NAMAA_DIALOGS` شيتات التأكيد بدل confirm/alert. `NAMAA_FX` الحركات والأصوات. `NAMAA_GA` Google Analytics. `NAMAA_ASK` «راشد» (المساعد: بيجاوب وبيسجّل بعد تأكيد).
   - `NAMAA_SMARTLOOK` (في الـ `<head>`) تسجيل جلسات Smartlook: الأرقام نجوم، الخانات والـ IP مش بيتسجلوا، وأي نص كتبه المستخدم (من `portfolioData`/`nm-budget`/`nm-plan`/`nm-name`) والشات بيتعلّم `data-sl="mask"`. التعريف برقم عشوائي `nm-slid`. بيقف لو `nm-hide` شغال، ومش بيتحمّل أصلًا لو `nm-sl-off`=1 (زرار «ساعدنا نحسّن نماء» في الإعدادات). كل `NamaaTrack` بيتبعت كمان كـ `smartlook('track')`. **أي شاشة جديدة فيها نص شخصي مش جاي من المفاتيح دي لازم تاخد `data-sl="mask"`.**
   - الباقي واضح من التعليق اللي في أول كل موديول.
3. **بين React والموديولات** فيه hooks على `window`: `__nmTab`, `__nmOpenMore(view)`, `__nmEdit(id)`, `__nmApply(data)`, `__nmDcRefresh()` (يعيد رسم React)، `__nmDC(n)`/`__nmCU()` (عملة العرض).

### البيانات (كلها في localStorage على الموبايل، مفيش سيرفر غير المزامنة)
`portfolioData` الأصول والعملات · `nm-budget` الميزانية والديون · `nm-plan` خطتي · `nm-learn` تعلّم · `nm-dcur` عملة العرض · `nm-tabs` الشريط · `nm-name` الاسم · `nm-ek` مفتاح التشفير (ماينفعش يتزامن) · `nm-slid` رقم Smartlook العشوائي.
- **نهاية العائد:** `yieldEndY/yieldEndM` بيتحسبوا بس لو `yieldEndCustom:true` (المستخدم اختار «ليه تاريخ نهاية» في المحرر). غير كده العائد بيكمّل لآخر «فترة الحساب» مهما اتمدّت. القيم القديمة المتسجّلة تلقائي بتتجاهل وقت الحساب، من غير migration.
- **بيع وإعادة شراء (لأصول التقييم بس):** `exitYears` (عدد السنين من `purchaseDate`، أو من بداية الفترة لو مفيش تاريخ)، `exitFeePct` (مصاريف الخروج %)، `exitTo` (`'reinvest'` أو id حساب). في `projection` شهر البيع: الرصيد × (1 − المصاريف). مع `reinvest` الرصيد بيكمّل، والإيجار الثابت بيتحسب من جديد بنفس نسبته للقيمة الأصلية، واللفة بتتكرر كل `exitYears`. لو `exitTo` حساب، الفلوس بتنزل فيه والأصل بيتصفّر ويقف. الأحداث في `row.exits` وبتظهر فوق خريطة الدخل.
- **التوقعات كدالة:** `runProj(sy,sm,ey,em)` جوه `InvestmentCalculator` بتحسب أي فترة، و`projection` بيستخدمها. `NamaaPeriod.open` بياخد `proj/goal/salary/fmt/onGoal/onSalary` وبيدوّر لحد 50 سنة على أول شهر `monthlyYield` يوصل للهدف (`passiveIncomeGoal`) أو لمجموع `income` في `nm-budget`. حدث GA4: `period_change{via:'goal'|'salary',months}`.
- **التقرير المفصّل** (الإعدادات ← «📊 تقرير مفصّل» ← `exportToExcel`): Excel فيه ملخص (فلوسك/على الورق، الديون، الدخل السلبي، سنة الوصول للهدف وللمرتب بـ `runProj` لـ 50 سنة) + الأصول + الإيجارات والعوائد + الأسهم + خطة البيع ومواعيده (20 سنة) + الميزانية + الديون + الإسقاط. الدخل في الشهر = متوسط أول 12 شهر من `yield_<id>`. على الـ APK (`NamaaAndroid.share` نص بس) بيتبعت كتقرير نصي `namaa-<date>.txt`. حدث GA4: `export_excel{sheets,as:'xlsx'|'text'}`.
- **سحب الأسعار (`NAMAA_NET` قبل سكريبت React):** `window.NamaaNet` فيه `jget` (GET بمهلة)، `scan(market,tickers,cols)` (POST لـ TradingView بمهلة)، `nget/njson/sym` (GET من خلال التطبيق `__nmGet(u,ms)` بمهلة)، و`egx(syms,cols)` (أسهم البورصة المصرية: الويب والتطبيق في نفس الوقت، وبيخلص أول ما كل رمز ياخد قيمة). `refreshAll` بيشغّل `fetchLiveRates` و`fetchStockPrices` مع بعض. `fetchLiveRates` بيسأل كل المصادر في نفس اللحظة (currency-api، TradingView على global/forex/cfd، وعلى أندرويد: TradingView من التطبيق، Yahoo، Google) وبيخلص أول ما كل عملة ومعدن ييجي من TradingView، أو كل المصادر ترد، أو 8 ثواني. ترتيب الدمج: TradingView ← Yahoo (الدولار بس) ← Google ← currency-api، وأي سعر يبعد أكتر من 10% عن currency-api بيترفض. الدهب والفضة بيتحسبوا بالدولار اللي ظاهر في التطبيق، وGoogle مش بيغطي على TradingView. التشخيص في `nm-fx-tv` و`nm-fx-cand` و`nm-stk-src` و`nm-xau`. اللوجوهات (`fetchLogos`) واسم السهم بعد الشراء (`lookupName` في `NAMAA_TRADE`) بيستخدموا `NamaaNet.egx` برضه. تفعيل عملة في الإعدادات بيسحب سعرها لوحده، وزرار «حدّث الأسعار» موجود في الرئيسية بس.
- **«فاحص الحلال»** (`viewMode==='halal'`): بيبعت السؤال لـ «راشد» بـ `NamaaAsk.open(src, سؤال)`؛ السؤال بيتبعت أول ما الشات يظهر (حتى بعد الموافقة أو اختيار المزوّد). حدث GA4: `ask_open{src:'halal'}`.
- **«راشد» (`NAMAA_ASK` v12، كان «اسأل نماء»):** بيجاوب من «لقطة» الحساب زي الأول، وكمان بيسجّل. السياق بيتبعت معاه `idsText()` (أرقام الأصول، أكواد أنواع الميزانية والديون والسلف، الدخل الثابت، العملات). الموديل بيرجّع بلوك ```` ```namaa {"actions":[…]} ``` ```` بالأنواع: `expense` `income` `asset_new` `asset_value` `stock_buy` `debt_new` `lent_new` `debt_pay` `lent_got`. `parseActs` بيفصل البلوك، و`norm` بيتحقق من كل سطر (مبلغ موجب، كود/رقم موجود، عملة ليها سعر) ويعمل كارت فيه «سجّل/عدّل/لأ» و«سجّل الكل». مفيش كتابة غير بعد «سجّل»، ومفيش مسح خالص. الكتابة بتعدّي على `NamaaBudget.add(kind,o)` (tx/debt/lent/pay/got، بنفس أشكال الشاشة) و`NamaaTrade.record({sym,qty,price,parent})` (نفس نواة الشراء `buyCore` اللي شاشة الشراء بتستخدمها) و`NamaaQuick.blank` لقالب الأصل. «تراجع» بيمسح التسجيل ده بعينه بس (`NamaaBudget.undo(kind,r)` أو حذف/استرجاع الأصل)، ولو اتعدّل بعدها بيرفض. اللي اتسجّل أو اتلغى بيتبعت للموديل في أول الرسالة الجاية «(من التطبيق: …)». موافقة جديدة `nm-ask-consent2` (لأن أسامي الديون والسلف بقت بتتبعت). `window.__nmRates()` بيسحب الأسعار لو اتفعّلت عملة. أحداث GA4: `rashed_propose{types,n}` `rashed_save{type,via:'one'|'all'}` `rashed_cancel{type}` `rashed_undo{type}`، وأحداث الشات القديمة `ask_*` زي ما هي.
- **منصات حسب السوق (31.1):** السوق بيتقري من `nm-onb.mk` (`EG` `SA` `AE` `XX`، ولو مفيش = مصر). في `NAMAA_PLAN` كل منصة في `PV` ليها `m:[أسواق]`، و`g` اختياري (`robo` مستثمر آلي، `screen` فحص أسهم، `debt` صكوك وتمويل بالدين، مش بيظهر في خطوة الطوارئ)، و`sb:1` لو لسه في بيئة تجريبية عند الجهة الرقابية. `chips(k,noRisk)` بيعرض اللي سوقه متختار بس، ولو فيه أكتر من سوق بيحط العلم جنب كل منصة. عناوين الفئات (`CL[].s`) ونصوص «إزاي» بتبقى عامة لو مصر مش من الأسواق. `guess()` بيقارن بعملة المستخدم الأساسية `nm-onb.cur`. «اشتريت من منصة؟» (`NAMAA_QUICKADD`) بيفلتر `P` بنفس الطريقة، والأصل بياخد عملة المنصة (`cur`: SAR/AED/USD) ويفعّلها ويسحب سعرها. `NamaaQuick.hint()` هو نص زرار الـ FAB. حدث GA4: `partner_click{option:<id المنصة>}` من زرار الشيت (المصري لسه بالأسامي القديمة). المصادر والتراخيص في نص كل منصة (`reg`)، ومحتاجة مراجعة كل كام شهر.
- **الرئيسية:** كارت «🎯 خطتي» وهو فاضي (`nm-plan-empty`) بيستخبى طول ما كارت «ابدأ مع نماء» ظاهر وفيه خطوة الخطة (`body.nm-onb-plan` من `NAMAA_ONBOARD`). خطوة «افتح نعمة اليوم» اتشالت من الخطوات.
- **اتشال في 30.9 (كان كود ميت):** عرض الكروت القديم `cardLayout==='legacy'` وشاشات التعديل اللي جواه، شاشة بحث الأسهم القديمة (`stockSearchOpen`)، أجزاء `false&&`، ومتغيرات ودوال مش مستخدمة. العروض الموجودة: `big` و`small` و`table` بس.
- **النسخة الكاملة** («⬇️ صدّر كل حاجة» ← `exportPortfolio`): JSON فيه المحفظة + `extra` بكل مفاتيح `NM_XK` (الميزانية، الخطة، الزكاة، تعلّم، نعمة اليوم، الاسم، الصورة، السجل، عملة العرض، المظهر، الشريط). مش فيه `nm-ek` ولا `nm-auth` ولا مفاتيح «اسأل نماء». الاستيراد (`fullImport`) بيطلب تأكيد، ويكتب المفاتيح ويعمل reload. الملفات القديمة من غير `extra` بتستورد المحفظة بس زي الأول. أحداث GA4: `backup_export{keys}` و`backup_import{keys,assets}`.

## خطوات أي تعديل ونشره
1. عدّل `index.html` (استبدال نص فريد، ومتعدّلش في حاجة مش متأكد منها).
2. جرّب في متصفح (Playwright) وخد صورة للشاشة.
3. `python3 tools/release.py <build> <version> "<ملاحظة بالعامية>"`: بيرفع `NM_BUILD`، يفحص كل السكريبتات بـ `node --check`، يرفض علامات ‹ ›، ويرفض أي كلمة في ملف `.leakwords` المحلي (حط فيه أسامي أصولك الحقيقية وأي مفاتيح؛ الملف مش بيترفع).
4. `git commit` و`git push`. الإصدار بيوصل للموبايلات لوحده.
- رقم الإصدار: `build` بيزيد 1 كل مرة، و`version` = `build/10` (مثلاً 283 ← 28.3).

## قواعد لازم تتحافظ عليها (من صاحب التطبيق)
- **ماتشيلش شيت تأكيد الحذف أبدًا** من غير ما تسأل. «تراجع» إضافة بعده، مش بديل.
- أي ميزة للأصل الرئيسي لازم تبقى للأصل الفرعي كمان والعكس.
- مفيش كود migration بيعدّل بيانات المستخدم (ضيّع أصول قبل كده).
- أي شيت أو نافذة `position:fixed` في React لازم `ReactDOM.createPortal(..., document.body)`.
- الأسهم: SVG بس، مش ‹ ›.
- الكلام كله بالعامية المصرية، والأرقام بفواصل (2,000,000).
- كل حدث GA4 جديد يتذكر اسمه والـ params بتاعته في الرد.

## أحداث GA4 الموجودة
`app_open` `app_resume` `app_updated` `app_error` `app_exit` · `onboarding_slide{slide}` `onboarding_goals_set` `onboarding_geo` `onboarding_complete` `onboarding_hide` · `asset_delete{sub}` `asset_reparent{to_root,new_group}` `subasset_created` `subasset_toast_back` `asset_view_change` · `snack_action{action,kind}` · `learn_rec_view{reason}` `learn_rec_click{reason}` `learn_video_play` `learn_video_complete` · `debt_*` · `plan_*` · `tabbar_*` · `transfer_cash_created` · `display_currency_set{currency}` `theme_change` `privacy_toggle` · `e2e_enabled` `e2e_migrated` · `update_available` `update_apply` …(القايمة الكاملة: دوّر على `NamaaTrack('` في `index.html`).

## الـ APK (للتغييرات الـ native بس)
- أي تعديل في الواجهة أو المنطق بيوصل بتحديث الويب، **من غير APK**.
- الـ APK محتاج يتعمل من جديد بس لو التغيير في `Bridge`/`MainActivity`/الأيقونات/الـ manifest.
- الطريقة: فك آخر APK بـ `apktool d`، وعدّل smali/manifest، وابنيه بـ `apktool b`، واعمله zipalign، ووقّعه بـ `apksigner` (alias `namaa`).
- `versionCode` = رقم الـ build، و`versionName` = رقم الإصدار، واسم الملف `namaa-<version>.apk`.
- **مفتاح التوقيع `namaa.keystore` مش في الريبو ولازم يفضل برا.** من غيره أي APK جديد مش هيتنزّل كتحديث فوق القديم. احفظه هو وكلمة سره في مكان آمن.
- الـ Bridge فيه `NamaaAndroid.setBg(color)` و`setIcon(theme)` (أيقونات: namaa, rausch, navy, teal, plum, amber) و`openUrl`, و`share`، وغيرهم.


## الثيمات (31.3–31.4)
- `window.__NM_THEMES`: ثيمات بلون واحد (a/p/s/r) + ثيمات 3 ألوان فيها `bg` (خلفية الصفحة) و`pop`/`op` (الزرار الأساسي ولون الكلام عليه) و`c3` (المربع في المظهر) و`ic` (أيقونة APK موجودة بتتستخدم بدالها).
- `laylid` (ليلي غامق) فيه `dark:1`: `window.__nmDark(true)` بيضيف `html.nm-dark` ويولّد `<style id="nm-dark-css">` بإعادة كتابة كل قواعد الـ CSS (ألوان الخلفية/الكلام/الحدود) بدالة `__nmDarkMap`، وMutationObserver بيظبط الـ inline styles وfill/stroke بتوع SVG. الخروج من الغامق بيعمل reload.
- عنصر عايز يفضل بألوانه في الغامق: حط عليه `data-nmk`. لو قاعدة محتاجة لون مخصوص في الغامق اكتبها بـ `html.nm-dark ...` (القواعد دي مش بيتعاد كتابتها).
