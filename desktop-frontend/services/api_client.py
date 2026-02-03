"""
API Client for Desktop Application.
Handles communication with Django backend.
"""
import requests
import json


class APIClient:
    """Client for interacting with the backend API."""
    
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def _get_headers(self):
        """Get request headers with authentication."""
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def login(self, username, password):
        """
        Login and obtain JWT tokens.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            dict: Response data with tokens
        """
        url = f'{self.base_url}/token/'
        data = {'username': username, 'password': password}
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        tokens = response.json()
        self.access_token = tokens['access']
        self.refresh_token = tokens['refresh']
        
        return tokens
    
    def register(self, username, email, password, role='viewer'):
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email
            password: Desired password
            role: User role (viewer or admin)
            
        Returns:
            dict: Response data
        """
        url = f'{self.base_url}/register/'
        data = {
            'username': username,
            'email': email,
            'password': password,
            'role': role
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def upload_csv(self, file_path):
        """
        Upload CSV file for analysis.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            dict: Analysis results
        """
        url = f'{self.base_url}/upload/'
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {}
            if self.access_token:
                headers['Authorization'] = f'Bearer {self.access_token}'
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
        
        return response.json()
    
    def get_summary(self):
        """
        Get summary of most recent dataset.
        
        Returns:
            dict: Summary data
        """
        url = f'{self.base_url}/summary/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_history(self):
        """
        Get upload history.
        
        Returns:
            dict: History data
        """
        url = f'{self.base_url}/history/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_dataset_detail(self, dataset_id):
        """
        Get detailed information about a dataset.
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            dict: Dataset details
        """
        url = f'{self.base_url}/dataset/{dataset_id}/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def download_report(self, dataset_id, save_path):
        """
        Download PDF report for a dataset.
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path to save the PDF
        """
        url = f'{self.base_url}/report/{dataset_id}/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
