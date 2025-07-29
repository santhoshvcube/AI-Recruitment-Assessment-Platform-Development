import os
import json
import logging
from typing import Dict, Any
from datetime import datetime
from jinja2 import Template
import weasyprint
from weasyprint import HTML, CSS

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Service for generating assessment reports in various formats.
    """
    
    def __init__(self):
        self.templates_dir = "app/templates"
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default report templates."""
        
        # HTML template for reports
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assessment Report - {{ candidate.name }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }
        .header .subtitle {
            color: #7f8c8d;
            font-size: 1.2em;
            margin-top: 10px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .score-container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }
        .score-item {
            flex: 1;
            min-width: 200px;
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            background: #f8f9fa;
        }
        .score-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .score-excellent { color: #27ae60; }
        .score-good { color: #f39c12; }
        .score-fair { color: #e67e22; }
        .score-poor { color: #e74c3c; }
        .recommendation {
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: bold;
            text-align: center;
            font-size: 1.2em;
        }
        .recommendation.strong-hire {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .recommendation.hire {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .recommendation.maybe {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        .recommendation.no-hire {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .list-item {
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            border-radius: 4px;
        }
        .metadata {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.9em;
            color: #6c757d;
            margin-top: 30px;
        }
        .two-column {
            display: flex;
            gap: 20px;
        }
        .column {
            flex: 1;
        }
        @media (max-width: 768px) {
            .two-column {
                flex-direction: column;
            }
            .score-container {
                flex-direction: column;
            }
        }
        @media print {
            body { margin: 0; padding: 15px; }
            .section { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Assessment Report</h1>
        <div class="subtitle">Comprehensive Candidate Evaluation</div>
    </div>

    <!-- Candidate Information -->
    <div class="section">
        <h2>Candidate Information</h2>
        <div class="two-column">
            <div class="column">
                <p><strong>Name:</strong> {{ candidate.name }}</p>
                <p><strong>Email:</strong> {{ candidate.email }}</p>
                {% if candidate.phone %}
                <p><strong>Phone:</strong> {{ candidate.phone }}</p>
                {% endif %}
            </div>
            <div class="column">
                <p><strong>Position:</strong> {{ job_description.title }}</p>
                <p><strong>Company:</strong> {{ job_description.company }}</p>
                <p><strong>Assessment Date:</strong> {{ assessment.created_at.strftime('%B %d, %Y') }}</p>
            </div>
        </div>
    </div>

    <!-- Overall Assessment -->
    <div class="section">
        <h2>Overall Assessment</h2>
        <div class="score-container">
            <div class="score-item">
                <div>Overall Score</div>
                <div class="score-value {% if assessment.overall_score >= 85 %}score-excellent{% elif assessment.overall_score >= 70 %}score-good{% elif assessment.overall_score >= 55 %}score-fair{% else %}score-poor{% endif %}">
                    {{ "%.1f"|format(assessment.overall_score or 0) }}%
                </div>
            </div>
            <div class="score-item">
                <div>Confidence Level</div>
                <div class="score-value {% if assessment.confidence_level >= 80 %}score-excellent{% elif assessment.confidence_level >= 60 %}score-good{% else %}score-fair{% endif %}">
                    {{ "%.1f"|format(assessment.confidence_level or 0) }}%
                </div>
            </div>
        </div>
        
        <div class="recommendation {{ assessment.hiring_recommendation|replace('_', '-') }}">
            Hiring Recommendation: {{ assessment.hiring_recommendation|replace('_', ' ')|title }}
        </div>
    </div>

    <!-- Component Scores -->
    <div class="section">
        <h2>Detailed Scores</h2>
        <div class="score-container">
            {% for component, score in assessment.component_scores.items() %}
            {% if score %}
            <div class="score-item">
                <div>{{ component|replace('_', ' ')|title }}</div>
                <div class="score-value {% if score >= 80 %}score-excellent{% elif score >= 65 %}score-good{% elif score >= 50 %}score-fair{% else %}score-poor{% endif %}">
                    {{ "%.1f"|format(score) }}%
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
    </div>

    <!-- Strengths -->
    <div class="section">
        <h2>Key Strengths</h2>
        {% for strength in assessment.strengths %}
        <div class="list-item">{{ strength }}</div>
        {% endfor %}
    </div>

    <!-- Development Areas -->
    <div class="section">
        <h2>Development Areas</h2>
        {% for area in assessment.development_areas %}
        <div class="list-item">{{ area }}</div>
        {% endfor %}
    </div>

    <!-- Risk Factors -->
    {% if assessment.risk_factors %}
    <div class="section">
        <h2>Risk Factors</h2>
        {% for risk in assessment.risk_factors %}
        <div class="list-item">
            <strong>{{ risk.type|replace('_', ' ')|title }}:</strong> {{ risk.description }}
            <br><em>Mitigation: {{ risk.mitigation }}</em>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Recommendations -->
    {% if assessment.recommendations %}
    <div class="section">
        <h2>Recommendations</h2>
        {% if assessment.recommendations.hiring_decision %}
        <p><strong>Hiring Decision:</strong> {{ assessment.recommendations.hiring_decision }}</p>
        {% endif %}
        {% if assessment.recommendations.next_steps %}
        <h3>Next Steps:</h3>
        {% for step in assessment.recommendations.next_steps %}
        <div class="list-item">{{ step }}</div>
        {% endfor %}
        {% endif %}
        {% if assessment.recommendations.development_plan %}
        <h3>Development Plan:</h3>
        {% for item in assessment.recommendations.development_plan %}
        <div class="list-item">{{ item }}</div>
        {% endfor %}
        {% endif %}
    </div>
    {% endif %}

    <!-- Skills Analysis -->
    <div class="section">
        <h2>Skills Analysis</h2>
        <div class="two-column">
            <div class="column">
                <h3>Technical Skills</h3>
                {% for category, skills in candidate.extracted_skills.technical_skills.items() %}
                {% if skills %}
                <p><strong>{{ category|replace('_', ' ')|title }}:</strong></p>
                <ul>
                {% for skill in skills[:5] %}
                <li>{{ skill }}</li>
                {% endfor %}
                </ul>
                {% endif %}
                {% endfor %}
            </div>
            <div class="column">
                <h3>Soft Skills</h3>
                <ul>
                {% for skill in candidate.extracted_skills.soft_skills[:8] %}
                <li>{{ skill }}</li>
                {% endfor %}
                </ul>
            </div>
        </div>
    </div>

    <!-- Interview Performance -->
    {% if metadata.include_interview_responses and interview_responses %}
    <div class="section">
        <h2>Interview Performance</h2>
        <p><strong>Total Questions:</strong> {{ interview_responses|length }}</p>
        {% for response in interview_responses[:3] %}
        <div class="list-item">
            <strong>Q{{ loop.index }}:</strong> {{ response.question.question[:100] }}...
            <br><strong>Score:</strong> {{ response.evaluation.overall_score }}/100
            <br><strong>Feedback:</strong> {{ response.evaluation.feedback[:200] }}...
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Metadata -->
    <div class="metadata">
        <p><strong>Report Generated:</strong> {{ metadata.generated_at }}</p>
        <p><strong>Generated By:</strong> {{ metadata.generated_by }}</p>
        <p><strong>Assessment ID:</strong> {{ assessment.id }}</p>
        <p><em>This report was generated by the AI Interview Assessment Platform. All scores and recommendations are based on automated analysis and should be considered alongside human judgment.</em></p>
    </div>
</body>
</html>
        """
        
        html_template_path = os.path.join(self.templates_dir, "assessment_report.html")
        if not os.path.exists(html_template_path):
            with open(html_template_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
    
    async def generate_pdf_report(self, report_data: Dict[str, Any], report_id: str, output_dir: str) -> str:
        """Generate PDF report from assessment data."""
        try:
            # First generate HTML
            html_content = await self._generate_html_content(report_data)
            
            # Convert HTML to PDF
            pdf_path = os.path.join(output_dir, f"{report_id}.pdf")
            
            # Create PDF with WeasyPrint
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(pdf_path)
            
            logger.info(f"PDF report generated: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise
    
    async def generate_html_report(self, report_data: Dict[str, Any], report_id: str, output_dir: str) -> str:
        """Generate HTML report from assessment data."""
        try:
            html_content = await self._generate_html_content(report_data)
            
            html_path = os.path.join(output_dir, f"{report_id}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {html_path}")
            return html_path
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            raise
    
    async def generate_json_report(self, report_data: Dict[str, Any], report_id: str, output_dir: str) -> str:
        """Generate JSON report from assessment data."""
        try:
            json_path = os.path.join(output_dir, f"{report_id}.json")
            
            # Convert datetime objects to strings for JSON serialization
            json_data = self._prepare_json_data(report_data)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON report generated: {json_path}")
            return json_path
            
        except Exception as e:
            logger.error(f"Error generating JSON report: {str(e)}")
            raise
    
    async def _generate_html_content(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML content from report data."""
        template_path = os.path.join(self.templates_dir, "assessment_report.html")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        # Render template with data
        html_content = template.render(**report_data)
        
        return html_content
    
    def _prepare_json_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for JSON serialization by converting datetime objects."""
        if isinstance(data, dict):
            return {key: self._prepare_json_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._prepare_json_data(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        else:
            return data

