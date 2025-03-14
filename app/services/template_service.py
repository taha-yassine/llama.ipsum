import json
import jinja2
from typing import Dict, Any, Optional
from pathlib import Path

class TemplateService:
    """Service for loading and rendering templates."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the template service.
        
        Args:
            template_dir: Optional custom template directory path
        """
        # Default template directory is within the app
        self.default_template_dir = Path(__file__).parent.parent / "templates"
        
        # Custom template directory (if provided)
        self.custom_template_dir = Path(template_dir) if template_dir else None
        
        # Set up the template environment with both directories
        loader = self._create_loader()
        self.env = jinja2.Environment(
            loader=loader,
            autoescape=False,  # Important for JSON templates
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def _create_loader(self) -> jinja2.BaseLoader:
        """Create a template loader that checks custom dir first, then default."""
        loaders = []
        
        # Add custom template directory if it exists
        if self.custom_template_dir and self.custom_template_dir.exists():
            loaders.append(jinja2.FileSystemLoader(str(self.custom_template_dir)))
        
        # Always add the default template directory
        loaders.append(jinja2.FileSystemLoader(str(self.default_template_dir)))
        
        return jinja2.ChoiceLoader(loaders)
    
    def render_template(self, template_path: str, **context) -> Dict[str, Any]:
        """
        Render a template with the given context and return as a Python dict.
        
        Args:
            template_path: Path to the template relative to template directory
            **context: Variables to pass to the template
            
        Returns:
            Rendered template as a Python dictionary
        """
        template = self.env.get_template(template_path)
        rendered = template.render(**context)
        return json.loads(rendered)
    
    def render_template_string(self, template_path: str, **context) -> str:
        """
        Render a template with the given context and return as a string.
        
        Args:
            template_path: Path to the template relative to template directory
            **context: Variables to pass to the template
            
        Returns:
            Rendered template as a string
        """
        template = self.env.get_template(template_path)
        return template.render(**context) 