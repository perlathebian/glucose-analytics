import os
from datetime import date
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


FONT_URL = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Regular.ttf"
FONT_BOLD_URL = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
FONT_PATH = "Amiri-Regular.ttf"
FONT_BOLD_PATH = "Amiri-Bold.ttf"


def download_arabic_font():
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(
            "Amiri-Regular.ttf not found. "
            "Download Amiri from https://fonts.google.com/specimen/Amiri "
            "and place Amiri-Regular.ttf and Amiri-Bold.ttf in the project root."
        )
    if not os.path.exists(FONT_BOLD_PATH):
        raise FileNotFoundError(
            "Amiri-Bold.ttf not found. "
            "Download Amiri from https://fonts.google.com/specimen/Amiri "
            "and place Amiri-Bold.ttf in the project root."
        )
    pdfmetrics.registerFont(TTFont("Cairo", FONT_PATH))
    pdfmetrics.registerFont(TTFont("Cairo-Bold", FONT_BOLD_PATH))

def ar(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def get_styles():
    return {
        "title_en": ParagraphStyle(
            "title_en",
            fontName="Cairo-Bold",
            fontSize=18,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=6,
            alignment=TA_CENTER,
        ),
        "title_ar": ParagraphStyle(
            "title_ar",
            fontName="Cairo-Bold",
            fontSize=16,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=12,
            alignment=TA_CENTER,
        ),
        "section_en": ParagraphStyle(
            "section_en",
            fontName="Cairo-Bold",
            fontSize=12,
            textColor=colors.HexColor("#16213e"),
            spaceBefore=14,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "section_ar": ParagraphStyle(
            "section_ar",
            fontName="Cairo-Bold",
            fontSize=11,
            textColor=colors.HexColor("#16213e"),
            spaceAfter=6,
            alignment=TA_RIGHT,
        ),
        "body_en": ParagraphStyle(
            "body_en",
            fontName="Cairo",
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "body_ar": ParagraphStyle(
            "body_ar",
            fontName="Cairo",
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            spaceAfter=4,
            alignment=TA_RIGHT,
        ),
        "warning": ParagraphStyle(
            "warning",
            fontName="Cairo-Bold",
            fontSize=10,
            textColor=colors.HexColor("#cc0000"),
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "warning_ar": ParagraphStyle(
            "warning_ar",
            fontName="Cairo-Bold",
            fontSize=10,
            textColor=colors.HexColor("#cc0000"),
            spaceAfter=4,
            alignment=TA_RIGHT,
        ),
    }


def divider(story):
    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%",
        thickness=0.5,
        color=colors.HexColor("#cccccc")
    ))
    story.append(Spacer(1, 6))


def build_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16213e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Cairo-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Cairo"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dddddd")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def generate_report(df):
    download_arabic_font()
    styles = get_styles()
    story = []
    output_path = "outputs/glucose_report.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # ── COVER ──────────────────────────────────────────────────
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("Glucose Monitoring Report", styles["title_en"]))
    story.append(Paragraph(ar("تقرير مراقبة مستوى السكر في الدم"), styles["title_ar"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        f"Generated: {date.today().strftime('%B %d, %Y')}",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar(f"تاريخ الإصدار: {date.today().strftime('%Y/%m/%d')}"),
        styles["body_ar"]
    ))
    story.append(Paragraph(
        f"Period: {df['timestamp'].min().strftime('%b %d')} – "
        f"{df['timestamp'].max().strftime('%b %d, %Y')}",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar("الفترة الزمنية: من 28 مارس إلى 11 أبريل 2026"),
        styles["body_ar"]
    ))
    divider(story)

    # ── PATIENT CONTEXT ────────────────────────────────────────
    story.append(Paragraph("Patient Context", styles["section_en"]))
    story.append(Paragraph(ar("السياق الطبي للمريض"), styles["section_ar"]))

    context_en = [
        "• Type 2 Diabetes — confirmed by C-peptide 0.71 ng/mL (normal range, pancreas still producing insulin)",
        "• HbA1c: 12.54% — severely uncontrolled",
        "• Anti-GAD antibodies: pending (autoimmune Type 1 not yet ruled out)",
        "• Active post-surgical inflammation (boil I&D)",
        "• Insulin regimen: Novorapid (pre-meal) + Lantus (basal, nightly)",
        "• Doctor's target: fasting/waking glucose below 130 mg/dL",
        "• Lipids: normal (Cholesterol 164, LDL 96, HDL 55, TG 69 mg/dL)",
        "• Kidneys: intact — Creatinine 0.67, uACR 11.19 mg/g (no nephropathy)",
        "• Liver: normal — AST 17, ALT 15 U/L",
        "• Note: some doses were skipped by patient during observation period",
    ]
    context_ar = [
        ar("• داء السكري من النوع الثاني — مؤكد بـ C-peptide 0.71 (طبيعي، البنكرياس لا يزال ينتج الأنسولين)"),
        ar("• HbA1c: 12.54% — غير متحكم به بشكل حاد"),
        ar("• أجسام مضادة Anti-GAD: نتيجة معلقة (النوع الأول المناعي لم يُستبعد بعد)"),
        ar("• التهاب نشط ما بعد الجراحة (شق وتصريف دملة)"),
        ar("• نظام الأنسولين: نوفورابيد (قبل الوجبات) + لانتوس (أساسي، ليلاً)"),
        ar("• هدف الطبيب: سكر الصيام/الصباح أقل من 130 mg/dL"),
        ar("• الدهون: طبيعية (كوليسترول 164، LDL 96، HDL 55، ثلاثيات الغليسريد 69 mg/dL)"),
        ar("• الكلى: سليمة — كرياتينين 0.67، uACR 11.19 (لا اعتلال كلوي)"),
        ar("• الكبد: طبيعي — AST 17، ALT 15 U/L"),
        ar("• ملاحظة: تم تخطي بعض الجرعات من قبل المريض خلال فترة المراقبة"),
    ]
    for en, a in zip(context_en, context_ar):
        story.append(Paragraph(en, styles["body_en"]))
        story.append(Paragraph(a, styles["body_ar"]))

    divider(story)

    # ── WAKING GLUCOSE STATS ───────────────────────────────────
    waking = df[df["waking_reading"] == 1]["glucose_mg_dl"].dropna()

    story.append(Paragraph("Waking Glucose Statistics", styles["section_en"]))
    story.append(Paragraph(ar("إحصاءات سكر الصباح عند الاستيقاظ"), styles["section_ar"]))

    in_range = int(((waking >= 70) & (waking <= 130)).sum())
    above_180 = int((waking > 180).sum())
    above_130 = int((waking > 130).sum())
    total_waking = len(waking)

    waking_data = [
        ["Metric", "Value", "Arabic / ملاحظة"],
        ["Total waking readings", str(total_waking), ar("إجمالي قراءات الصباح")],
        ["Mean", f"{waking.mean():.1f} mg/dL", ar("المتوسط")],
        ["Median", f"{waking.median():.1f} mg/dL", ar("الوسيط")],
        ["Std Deviation", f"{waking.std():.1f} mg/dL", ar("الانحراف المعياري")],
        ["Min / Max", f"{waking.min():.0f} / {waking.max():.0f} mg/dL", ar("الأدنى / الأعلى")],
        ["Above 180 mg/dL", f"{above_180} / {total_waking} days", ar("فوق 180 (ارتفاع)")],
        ["Above 130 mg/dL", f"{above_130} / {total_waking} days", ar("فوق 130 (خارج الهدف)")],
        ["In target (70–130)", f"{in_range} / {total_waking} days", ar("ضمن النطاق المستهدف")],
    ]
    story.append(build_table(waking_data, col_widths=[6 * cm, 4 * cm, 7 * cm]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "⚠ Target range achieved on 0 of 11 initial mornings. "
        "First target readings appeared after lantus was increased to 18 units.",
        styles["warning"]
    ))
    story.append(Paragraph(
        ar("⚠ لم يتم تحقيق النطاق المستهدف في أي من الأيام الـ11 الأولى. "
           "أول قراءات ضمن الهدف ظهرت بعد رفع جرعة لانتوس إلى 18 وحدة."),
        styles["warning_ar"]
    ))
    divider(story)

    # ── LANTUS TABLE ───────────────────────────────────────────
    story.append(Paragraph("Lantus Dose vs Next Morning Glucose", styles["section_en"]))
    story.append(Paragraph(ar("جرعة لانتوس مقابل سكر الصباح التالي"), styles["section_ar"]))

    story.append(Paragraph(
        "Higher lantus doses consistently produce lower waking glucose. "
        "The skipped dose (0 units) directly resulted in the highest recent waking reading (208 mg/dL).",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar("الجرعات الأعلى من لانتوس تنتج باستمرار سكراً صباحياً أقل. "
           "تخطي الجرعة (0 وحدة) أدى مباشرة إلى أعلى قراءة صباحية مؤخراً (208 mg/dL)."),
        styles["body_ar"]
    ))

    lantus_data = [
        ["Lantus Units", "Next Waking Glucose", ar("الجرعة / النتيجة")],
        ["12", "293 mg/dL", ar("12 وحدة ← 293")],
        ["14", "242, 197, 246, 198 mg/dL", ar("14 وحدة ← متوسط 221")],
        ["16", "164, 200, 152, 187, 170 mg/dL", ar("16 وحدة ← متوسط 175")],
        ["18", "183, 110, 122 mg/dL", ar("18 وحدة ← متوسط 138")],
        ["0 (skipped)", "208 mg/dL", ar("0 (تخطي) ← 208")],
    ]
    story.append(build_table(lantus_data, col_widths=[4 * cm, 7 * cm, 6 * cm]))
    divider(story)

    # ── NOVORAPID EFFECTIVENESS ────────────────────────────────
    story.append(Paragraph("Novorapid Effectiveness", styles["section_en"]))
    story.append(Paragraph(ar("فعالية نوفورابيد"), styles["section_ar"]))

    novo_data = [
        ["Dose", "Mean Glucose Change", ar("الجرعة / التأثير")],
        ["2 units", "+74.0 mg/dL", ar("2 وحدة ← ارتفاع 74")],
        ["6 units", "+9.4 mg/dL", ar("6 وحدات ← ارتفاع طفيف")],
        ["7 units", "+29.5 mg/dL", ar("7 وحدات ← ارتفاع")],
        ["8 units", "-43.8 mg/dL ✓", ar("8 وحدات ← انخفاض فعّال")],
    ]
    story.append(build_table(novo_data, col_widths=[4 * cm, 6 * cm, 7 * cm]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "61.5% of injections successfully lowered glucose. "
        "Only 8-unit doses produce consistent reduction. "
        "Doses of 6–7 units are largely ineffective for this patient.",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar("61.5% من الحقن خفضت السكر بنجاح. "
           "فقط جرعة 8 وحدات تنتج انخفاضاً ثابتاً. "
           "جرعات 6-7 وحدات غير فعّالة إلى حد بعيد لهذا المريض."),
        styles["body_ar"]
    ))
    divider(story)

    # ── MEAL SPIKE ─────────────────────────────────────────────
    story.append(Paragraph("Glucose Change by Meal", styles["section_en"]))
    story.append(Paragraph(ar("تغير السكر حسب الوجبة"), styles["section_ar"]))

    meal_data = [
        ["Meal", "Mean Change", "Interpretation", ar("التفسير")],
        ["Breakfast", "+13.7 mg/dL",
         "Rises despite insulin", ar("يرتفع رغم الأنسولين")],
        ["Lunch", "-35.7 mg/dL",
         "Moderate reduction", ar("انخفاض معتدل")],
        ["Dinner", "-35.8 mg/dL",
         "Effective reduction", ar("انخفاض فعّال")],
    ]
    story.append(build_table(meal_data,
                             col_widths=[3.5 * cm, 3.5 * cm, 5 * cm, 5 * cm]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Breakfast is the most problematic meal. The dawn phenomenon "
        "(cortisol/adrenaline spike on waking) raises glucose before breakfast, "
        "and breakfast further raises it despite pre-meal novorapid.",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar("الفطور هو الوجبة الأكثر إشكالية. ظاهرة الفجر (ارتفاع الكورتيزول والأدرينالين "
           "عند الاستيقاظ) ترفع السكر قبل الفطور، والفطور يرفعه أكثر رغم نوفورابيد."),
        styles["body_ar"]
    ))
    divider(story)

    # ── PREDICTION ─────────────────────────────────────────────
    story.append(Paragraph("Predictive Model", styles["section_en"]))
    story.append(Paragraph(ar("النموذج التنبؤي"), styles["section_ar"]))

    story.append(Paragraph(
        "Ridge regression trained on lantus dose and previous waking glucose. "
        "Evaluated with leave-one-out cross-validation (appropriate for small datasets).",
        styles["body_en"]
    ))
    story.append(Paragraph(
        ar("انحدار ريدج مدرَّب على جرعة لانتوس وسكر الصباح السابق. "
           "تم التقييم بالتحقق المتقاطع leave-one-out (مناسب للبيانات الصغيرة)."),
        styles["body_ar"]
    ))

    pred_data = [
        ["Parameter", "Value", ar("المعامل / القيمة")],
        ["Training pairs", "13", ar("13 زوجاً تدريبياً")],
        ["Mean Absolute Error", "33.8 mg/dL", ar("متوسط الخطأ المطلق: 33.8")],
        ["Lantus coefficient", "-18.16", ar("معامل لانتوس: -18.16 (كلما زادت الجرعة انخفض السكر)")],
        ["Prev waking coefficient", "+18.52", ar("معامل سكر أمس: +18.52 (كلما ارتفع أمس ارتفع اليوم)")],
        ["Prediction Apr 12", "166.7 mg/dL ± 33.8", ar("توقع 12 أبريل: 166.7 ± 33.8 mg/dL")],
    ]
    story.append(build_table(pred_data, col_widths=[5 * cm, 5 * cm, 7 * cm]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "⚠ This is a directional estimate only, not a clinical measurement. "
        "Do not adjust insulin doses based on this prediction alone.",
        styles["warning"]
    ))
    story.append(Paragraph(
        ar("⚠ هذا تقدير اتجاهي فقط وليس قياساً سريرياً. "
           "لا تعدّل جرعات الأنسولين بناءً على هذا التوقع وحده."),
        styles["warning_ar"]
    ))

    story.append(PageBreak())

    # ── PLOTS ──────────────────────────────────────────────────
    plot_files = [
        ("outputs/glucose_timeline.png",
         "Glucose Timeline",
         ar("مخطط مستوى السكر عبر الزمن")),
        ("outputs/daily_average.png",
         "Daily Average Glucose",
         ar("متوسط السكر اليومي")),
        ("outputs/hourly_distribution.png",
         "Hourly Distribution",
         ar("التوزيع حسب ساعة اليوم")),
        ("outputs/insulin_response.png",
         "Novorapid Dose vs Glucose Response",
         ar("جرعة نوفورابيد مقابل استجابة السكر")),
    ]

    story.append(Paragraph("Visual Analysis", styles["section_en"]))
    story.append(Paragraph(ar("التحليل البصري"), styles["section_ar"]))
    story.append(Spacer(1, 0.3 * cm))

    for path, title_en, title_ar_text in plot_files:
        if os.path.exists(path):
            story.append(Paragraph(title_en, styles["section_en"]))
            story.append(Paragraph(title_ar_text, styles["section_ar"]))
            story.append(Image(path, width=17 * cm, height=7 * cm))
            story.append(Spacer(1, 0.5 * cm))

    doc.build(story)
    print(f"Report saved: {output_path}")
    return output_path