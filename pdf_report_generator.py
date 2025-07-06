import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import matplotlib.pyplot as plt
import numpy as np

class GeneticReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        # Baslik stili - optimize edilmis spacing
        self.title_style = ParagraphStyle(
            'CustomTitle', 
            parent=self.styles['Title'],
            fontSize=20, 
            spaceAfter=20,  # Azaltildi
            spaceBefore=10, # Azaltildi
            textColor=HexColor('#2C3E50'), 
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=24
        )
        
        # Alt baslik stili - optimize edilmis spacing
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle', 
            parent=self.styles['Heading2'],
            fontSize=14, 
            spaceAfter=12,  # Azaltildi
            spaceBefore=15, # Azaltildi
            textColor=HexColor('#3498DB'), 
            fontName='Helvetica-Bold',
            leading=16
        )
        
        # Normal metin stili - optimize edilmis
        self.body_style = ParagraphStyle(
            'CustomBody', 
            parent=self.styles['Normal'],
            fontSize=10, 
            spaceAfter=8,   # Azaltildi
            spaceBefore=3,  # Azaltildi
            textColor=black, 
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=12,
            leftIndent=0,
            rightIndent=0
        )
        
        # Vurgu stili
        self.highlight_style = ParagraphStyle(
            'Highlight', 
            parent=self.styles['Normal'],
            fontSize=11, 
            spaceAfter=8,   # Azaltildi
            spaceBefore=5,  # Azaltildi
            textColor=HexColor('#E74C3C'), 
            fontName='Helvetica-Bold',
            leading=13
        )
        
        # Yorum stili - yapay zeka yorumlari icin
        self.comment_style = ParagraphStyle(
            'Comment',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=8,   # Azaltildi
            spaceBefore=5,  # Azaltildi
            textColor=HexColor('#2C3E50'),
            fontName='Helvetica',
            leading=11,
            leftIndent=10,
            rightIndent=10,
            alignment=TA_JUSTIFY
        )

    def create_header_footer(self, canvas_obj, doc):
        canvas_obj.saveState()
        
        # Header
        header_y = A4[1] - 50
        canvas_obj.setFont('Helvetica-Bold', 12)  # Font boyutu kucultuldu
        canvas_obj.setFillColor(HexColor('#2C3E50'))
        canvas_obj.drawString(50, header_y, "🧬 Genetik Varyant Analiz Raporu")
        
        # Header cizgisi
        canvas_obj.setStrokeColor(HexColor('#3498DB'))
        canvas_obj.setLineWidth(1)  # cizgi kalinligi azaltildi
        canvas_obj.line(50, header_y - 8, A4[0] - 50, header_y - 8)
        
        # Footer
        footer_y = 30  # Biraz yukari tasindi
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(HexColor('#7F8C8D'))
        canvas_obj.drawString(50, footer_y, f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        canvas_obj.drawRightString(A4[0] - 50, footer_y, f"Sayfa {doc.page}")
        
        canvas_obj.restoreState()

    def create_summary_chart(self, results_df):
        plt.rcParams['font.family'] = ['DejaVu Sans']
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Boyut kucultuldu
        axes = axes.flatten()
        fig.suptitle('Genetik Varyant Analiz Özeti', fontsize=14, fontweight='bold', y=0.95)
        
        # Klinik önemi dagilimi
        if 'CLNSIG' in results_df.columns and not results_df['CLNSIG'].isna().all():
            cl_counts = results_df['CLNSIG'].value_counts()
            if not cl_counts.empty:
                axes[0].pie(cl_counts.values, labels=cl_counts.index, autopct='%1.1f%%', startangle=90)
                axes[0].set_title('Klinik Önemi Dagilimi', fontweight='bold', pad=15)
            else:
                axes[0].text(0.5, 0.5, 'Veri yok', ha='center', va='center', transform=axes[0].transAxes)
        else:
            axes[0].text(0.5, 0.5, 'CLNSIG verisi bulunamadi', ha='center', va='center', transform=axes[0].transAxes)
        
        # Kromozom dagilimi
        if 'CHROM' in results_df.columns:
            chr_counts = results_df['CHROM'].value_counts().head(10)
            if not chr_counts.empty:
                axes[1].bar(range(len(chr_counts)), chr_counts.values)
                axes[1].set_xticks(range(len(chr_counts)))
                axes[1].set_xticklabels(chr_counts.index.astype(str), rotation=45)
                axes[1].set_title('Kromozom Dagilimi', fontweight='bold', pad=15)
                axes[1].set_xlabel('Kromozom')
                axes[1].set_ylabel('Varyant Sayisi')
            else:
                axes[1].text(0.5, 0.5, 'Veri yok', ha='center', va='center', transform=axes[1].transAxes)
        
        # Allel frekansi dagilimi
        if 'PopMax_AF' in results_df.columns:
            af_data = pd.to_numeric(results_df['PopMax_AF'], errors='coerce').dropna()
            if not af_data.empty and len(af_data) > 1:
                axes[2].hist(af_data, bins=min(20, len(af_data)), alpha=0.7)
                axes[2].set_title('Allel Frekansi Dagilimi', fontweight='bold', pad=15)
                axes[2].set_xlabel('PopMax AF')
                axes[2].set_ylabel('Varyant Sayisi')
            else:
                axes[2].text(0.5, 0.5, 'AF verisi yetersiz', ha='center', va='center', transform=axes[2].transAxes)
        else:
            axes[2].text(0.5, 0.5, 'PopMax_AF verisi yok', ha='center', va='center', transform=axes[2].transAxes)
        
        # Gen bazli dagilim
        if 'GENE' in results_df.columns:
            gene_counts = results_df['GENE'].value_counts().head(10)
            if not gene_counts.empty:
                y_pos = range(len(gene_counts))
                axes[3].barh(y_pos, gene_counts.values)
                axes[3].set_yticks(y_pos)
                axes[3].set_yticklabels(gene_counts.index)
                axes[3].set_title('En Sik Görulen Genler', fontweight='bold', pad=15)
                axes[3].set_xlabel('Varyant Sayisi')
            else:
                axes[3].text(0.5, 0.5, 'Gen verisi yok', ha='center', va='center', transform=axes[3].transAxes)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG', dpi=300, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        plt.close()
        
        return buf

    def generate_report(self, results_df, patient_info=None, output_filename="genetic_report.pdf", report_options=None):
        if report_options is None:
            report_options = {'template': 'Standart Rapor', 'include_charts': True, 'include_detailed_analysis': True}
        
        # Sayfa ayarlari - margin'lar optimize edildi
        doc = SimpleDocTemplate(
            output_filename, 
            pagesize=A4,
            rightMargin=50, 
            leftMargin=50,
            topMargin=70,   # Header icin yer
            bottomMargin=50
        )
        
        story = []
        
        # Ana baslik
        story.append(Paragraph("Genetik Varyant Analiz Raporu", self.title_style))
        story.append(Spacer(1, 15))  # Azaltildi
        
        # Hasta bilgileri
        if patient_info:
            story.append(Paragraph("Hasta Bilgileri", self.subtitle_style))
            
            table_data = [
                ["Hasta ID:", str(patient_info.get('id', 'N/A'))],
                ["Hasta Adi:", str(patient_info.get('name', 'N/A'))],
                ["Yas:", str(patient_info.get('age', 'N/A'))],
                ["Test Tarihi:", str(patient_info.get('test_date', 'N/A'))],
                ["Rapor Tarihi:", datetime.now().strftime('%d.%m.%Y %H:%M')],
                ["Toplam Varyant:", str(len(results_df))]
            ]
            
            patient_table = Table(table_data, colWidths=[2.2*inch, 3.3*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#DEE2E6')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 20))  # Azaltildi
        
        # Özet grafik
        if report_options.get('include_charts', True):
            story.append(Paragraph("Analiz Özeti", self.subtitle_style))
            
            try:
                img_buf = self.create_summary_chart(results_df)
                img = Image(img_buf, width=6*inch, height=4*inch)  # Boyut kucultuldu
                story.append(img)
                story.append(Spacer(1, 15))  # Azaltildi
            except Exception as e:
                error_msg = f"Grafik olusturulamadi: {str(e)}"
                story.append(Paragraph(error_msg, self.body_style))
                story.append(Spacer(1, 10))
        
        # Klinik önem analizi
        story.append(Paragraph("Klinik Önem Analizi", self.subtitle_style))
        
        if 'CLNSIG' in results_df.columns:
            # Pathogenic varyantlar
            pathogenic_variants = results_df[results_df['CLNSIG'].str.contains('Pathogenic', na=False, case=False)]
            if not pathogenic_variants.empty:
                story.append(Paragraph(f"⚠️ Yuksek Risk Varyantlari: {len(pathogenic_variants)} adet", self.highlight_style))
                story.append(Paragraph(
                    "Bu varyantlar hastalik gelisimi ile guclu iliskilidir ve klinik takip gerektirir.", 
                    self.body_style
                ))
                story.append(Spacer(1, 8))
            
            # Benign varyantlar
            benign_variants = results_df[results_df['CLNSIG'].str.contains('Benign', na=False, case=False)]
            if not benign_variants.empty:
                story.append(Paragraph(f"✅ Dusuk Risk Varyantlari: {len(benign_variants)} adet", self.body_style))
                story.append(Spacer(1, 8))
            
            # Uncertain varyantlar
            uncertain_variants = results_df[results_df['CLNSIG'].str.contains('Uncertain', na=False, case=False)]
            if not uncertain_variants.empty:
                story.append(Paragraph(f"❓ Belirsiz Önemi Olan Varyantlar: {len(uncertain_variants)} adet", self.body_style))
                story.append(Spacer(1, 15))
        else:
            story.append(Paragraph("Klinik önem verisi bulunamadi.", self.body_style))
            story.append(Spacer(1, 15))
        
        # Detayli varyant listesi
        story.append(Paragraph("Detayli Varyant Listesi", self.subtitle_style))
        
        # Tablo icin sutunlari sec
        display_columns = ['CHROM', 'POS', 'REF', 'ALT', 'GENE', 'CLNSIG']
        available_columns = [col for col in display_columns if col in results_df.columns]
        
        if available_columns:
            # Maksimum 15 varyant göster
            display_limit = min(15, len(results_df))
            table_data = [available_columns]  # Header
            
            for _, row in results_df.head(display_limit).iterrows():
                row_data = []
                for col in available_columns:
                    value = str(row.get(col, 'N/A'))
                    # Uzun degerleri kisalt
                    if len(value) > 15:
                        value = value[:12] + "..."
                    row_data.append(value)
                table_data.append(row_data)
            
            # Sutun genisliklerini hesapla
            col_widths = [inch * 0.75] * len(available_columns)
            if len(available_columns) <= 4:
                col_widths = [inch * 1.2] * len(available_columns)
            
            variant_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            variant_table.setStyle(TableStyle([
                # Header stil
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Data stil
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
                ('TEXTCOLOR', (0, 1), (-1, -1), black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                
                # Genel
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#DEE2E6')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(variant_table)
            
            if len(results_df) > display_limit:
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    f"Not: Sadece ilk {display_limit} varyant gösterilmistir. Toplam {len(results_df)} varyant analiz edilmistir.",
                    self.body_style
                ))
        else:
            story.append(Paragraph("Göruntulenecek varyant verisi bulunamadi.", self.body_style))
        
        story.append(PageBreak())
        
        # Yapay zeka yorumlari - sadece varsa
        if report_options.get('include_detailed_analysis', True) and 'Gemini_Yorum' in results_df.columns:
            story.append(Paragraph("Yapay Zeka Yorumlari", self.subtitle_style))
            
            comment_limit = len(results_df)
            for idx, (_, row) in enumerate(results_df.iterrows(), 1):
                # Varyant basligi
                variant_info = f"Varyant {idx}: {row.get('CHROM', 'N/A')}:{row.get('POS', 'N/A')} {row.get('REF', 'N/A')}>{row.get('ALT', 'N/A')}"
                if 'GENE' in row and pd.notna(row['GENE']):
                    variant_info += f" ({row['GENE']})"
                
                story.append(Paragraph(variant_info, self.subtitle_style))
                
                # Yorum metni
                comment_text = str(row.get('Gemini_Yorum', 'Yorum bulunamadi'))
                # cok uzun yorumlari kisalt
                if len(comment_text) > 2000:  # Limit azaltildi
                    comment_text = comment_text[:2000] + "... (Yorum kisaltilmistir)"
                
                story.append(Paragraph(comment_text, self.comment_style))
                story.append(Spacer(1, 12))  # Azaltildi
        
        # Sadece yorum varsa sayfa sonu ekle
        if report_options.get('include_detailed_analysis', True) and 'Gemini_Yorum' in results_df.columns:
            story.append(PageBreak())
        
        # Sonuc ve öneriler
        story.append(Paragraph("Sonuc ve Öneriler", self.subtitle_style))
        
        conclusion_text = f"""
        Bu rapor, {len(results_df)} genetik varyantin kapsamli analizini icermektedir. 
        Analiz sonuclari, guncel bilimsel literatur ve klinik veritabanlari temel alinarak hazirlanmistir.
        <br/><br/>
        <b>Önemli Notlar:</b><br/>
        • Bu rapor bilgi amaclidir ve kesin tani koymaz<br/>
        • Klinik kararlar icin mutlaka uzman hekim görusu alinmalidir<br/>
        • Genetik danismanlik önerilir<br/>
        • Bu analiz mevcut bilimsel veriler isiginda yapilmistir
        """
        
        story.append(Paragraph(conclusion_text, self.body_style))
        story.append(Spacer(1, 20))
        
        # Footer bilgisi
        footer_text = "Bu rapor otomatik olarak olusturulmustur. Sorulariniz icin genetik uzmaniniza danisiniz."
        footer_style = ParagraphStyle(
            'Footer', 
            parent=self.styles['Normal'], 
            fontSize=8, 
            textColor=HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=0
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # PDF'i olustur
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return output_filename

# Streamlit icin yardimci fonksiyon
def create_pdf_report_for_streamlit(results_df, patient_info=None, report_options=None):
    """Streamlit icin optimize edilmis PDF rapor olusturucu"""
    generator = GeneticReportGenerator()
    
    if report_options is None:
        report_options = {
            'template': 'Standart Rapor', 
            'include_charts': True, 
            'include_detailed_analysis': True
        }
    
    import tempfile
    import os
    
    # Gecici dosya olustur
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Raporu olustur
        if report_options['template'] == 'Standart Rapor':
            # Standart rapor icin ilk 20 varyant
            df_to_use = results_df.head(20)
        else:
            # Tam rapor icin tum varyantlar
            df_to_use = results_df
        
        generator.generate_report(
            df_to_use, 
            patient_info, 
            temp_filename, 
            report_options
        )
        
        # PDF verisini oku
        with open(temp_filename, 'rb') as f:
            pdf_data = f.read()
        
        return pdf_data
        
    finally:
        # Gecici dosyayi temizle
        if os.path.exists(temp_filename):
            os.remove(temp_filename)