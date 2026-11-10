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
   - `NAMAA_SNACK` الرسالة الصغيرة تحت + «تراجع». `NAMAA_DIALOGS` شيتات التأكيد بدل confirm/alert. `NAMAA_FX` الحركات والأصوات. `NAMAA_GA` Google Analytics. `NAMAA_ASK` «اسأل نماء».
   - `NAMAA_SMARTLOOK` (في الـ `<head>`) تسجيل جلسات Smartlook: الأرقام نجوم، الخانات والـ IP مش بيتسجلوا، وأي نص كتبه المستخدم (من `portfolioData`/`nm-budget`/`nm-plan`/`nm-name`) والشات بيتعلّم `data-sl="mask"`. التعريف برقم عشوائي `nm-slid`. بيقف لو `nm-hide` شغال، ومش بيتحمّل أصلًا لو `nm-sl-off`=1 (زرار «ساعدنا نحسّن نماء» في الإعدادات). كل `NamaaTrack` بيتبعت كمان كـ `smartlook('track')`. **أي شاشة جديدة فيها نص شخصي مش جاي من المفاتيح دي لازم تاخد `data-sl="mask"`.**
   - الباقي واضح من التعليق اللي في أول كل موديول.
3. **بين React والموديولات** فيه hooks على `window`: `__nmTab`, `__nmOpenMore(view)`, `__nmEdit(id)`, `__nmApply(data)`, `__nmDcRefresh()` (يعيد رسم React)، `__nmDC(n)`/`__nmCU()` (عملة العرض).

### البيانات (كلها في localStorage على الموبايل، مفيش سيرفر غير المزامنة)
`portfolioData` الأصول والعملات · `nm-budget` الميزانية والديون · `nm-plan` خطتي · `nm-learn` تعلّم · `nm-dcur` عملة العرض · `nm-tabs` الشريط · `nm-name` الاسم · `nm-ek` مفتاح التشفير (ماينفعش يتزامن) · `nm-slid` رقم Smartlook العشوائي.

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
