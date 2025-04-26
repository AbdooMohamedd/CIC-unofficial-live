from abc import ABC, abstractmethod
from datetime import datetime

class ResponseComponent(ABC):
    @abstractmethod
    def get_content(self):
        pass

class BaseResponse(ResponseComponent):
    def __init__(self, content):
        self._content = content
    
    def get_content(self):
        return self._content

class ResponseDecorator(ResponseComponent):
    def __init__(self, response_component):
        self._response_component = response_component
    
    @abstractmethod
    def get_content(self):
        pass

class TimestampDecorator(ResponseDecorator):
    def get_content(self):
        base_content = self._response_component.get_content()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if isinstance(base_content, dict):
            base_content['timestamp'] = timestamp
            return base_content
        else:
            return f"{base_content}\n[Response generated at: {timestamp}]"

class LoggingDecorator(ResponseDecorator):
    def get_content(self):
        base_content = self._response_component.get_content()
        print(f"LOG: Response generated - {datetime.now()}")
        return base_content

class FormattingDecorator(ResponseDecorator):
    def get_content(self):
        base_content = self._response_component.get_content()
        
        if isinstance(base_content, str):
            # Apply some basic formatting to the string
            formatted = base_content.replace("**", "").strip()
            return formatted
        elif isinstance(base_content, dict):
            if 'response' in base_content:
                base_content['response'] = base_content['response'].replace("**", "").strip()
            return base_content
        return base_content