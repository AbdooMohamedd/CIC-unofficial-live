from abc import ABC, abstractmethod

class ResponseHandler(ABC):
    @abstractmethod
    def process_response(self, query, response):
        pass
    
class StandardResponseHandler(ResponseHandler):
    def process_response(self, query, response):
        return {
            'query': query,
            'response': response,
            'type': 'standard'
        }

class TechnicalResponseHandler(ResponseHandler):
    def process_response(self, query, response):
        return {
            'query': query,
            'response': response,
            'type': 'technical',
            'technical_keywords': self._extract_technical_keywords(response)
        }
    
    def _extract_technical_keywords(self, response):
        # Simple implementation - in a real system, this could use NLP
        technical_terms = ['error', 'bug', 'code', 'system', 'update', 
                          'installation', 'software', 'hardware', 'configuration']
        return [term for term in technical_terms if term.lower() in response.lower()]

class FeedbackResponseHandler(ResponseHandler):
    def process_response(self, query, response):
        return {
            'query': query,
            'response': response,
            'type': 'feedback',
            'sentiment': self._analyze_sentiment(query)
        }
    
    def _analyze_sentiment(self, query):
        # Simple sentiment analysis - would use proper NLP in production
        positive_words = ['good', 'great', 'excellent', 'awesome', 'thanks', 'helpful']
        negative_words = ['bad', 'poor', 'terrible', 'unhelpful', 'disappointed']
        
        query_lower = query.lower()
        positive_count = sum(1 for word in positive_words if word in query_lower)
        negative_count = sum(1 for word in negative_words if word in query_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

class ResponseFactory:
    @staticmethod
    def create_handler(query):
        # Determine the type of handler based on the query
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['how to', 'error', 'problem', 'doesn\'t work']):
            return TechnicalResponseHandler()
        elif any(term in query_lower for term in ['thank', 'thanks', 'good', 'bad', 'review', 'rate']):
            return FeedbackResponseHandler()
        else:
            return StandardResponseHandler()