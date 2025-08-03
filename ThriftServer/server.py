# server.py
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import uuid
from datetime import datetime

# Add the generated Python Thrift code to the system path
sys.path.insert(0, os.path.abspath('gen-py'))

from server_service import VersionService
from server_service.ttypes import ResearchItem, ResearchItemType, CatalogFilter
from thrift.protocol import TJSONProtocol
from thrift.server import THttpServer
from thrift.transport import TTransport

class VersionServiceHandler:
    def __init__(self):
        # Initialize sample catalog data
        self.catalog_items = [
            ResearchItem(
                id="1",
                title="ResNet-50 Image Classification",
                description="Run ResNet-50 image classification remotely through ICE HPC using Cybershuttle",
                type=ResearchItemType.REPOSITORY,
                tags=["image-classification", "deep-learning", "resnet", "pytorch"],
                authors=["ssaghi3@gatech.edu", "swert6@gatech.edu", "pkadekodi3@gatech.edu"],
                createdAt="2024-01-15T10:30:00Z",
                updatedAt="2024-01-20T14:20:00Z"
            ),
            ResearchItem(
                id="2",
                title="CIFAR-10 Dataset",
                description="Complete CIFAR-10 dataset for image classification tasks with 60,000 32x32 color images",
                type=ResearchItemType.DATASET,
                tags=["image-classification", "computer-vision", "cifar", "benchmark"],
                authors=["dataset@cs.toronto.edu", "vision-lab@stanford.edu"],
                createdAt="2024-01-10T08:15:00Z",
                updatedAt="2024-01-10T08:15:00Z"
            ),
            ResearchItem(
                id="3",
                title="Transformer Language Model",
                description="Pre-trained transformer model for natural language processing tasks",
                type=ResearchItemType.MODEL,
                tags=["nlp", "transformer", "language-model", "bert"],
                authors=["nlp-team@google.com", "research@openai.com"],
                createdAt="2024-01-12T16:45:00Z",
                updatedAt="2024-01-18T11:30:00Z"
            ),
            ResearchItem(
                id="4",
                title="Deep Learning Tutorial Notebook",
                description="Comprehensive Jupyter notebook tutorial covering deep learning fundamentals with PyTorch",
                type=ResearchItemType.NOTEBOOK,
                tags=["tutorial", "deep-learning", "pytorch", "jupyter"],
                authors=["education@pytorch.org", "tutorials@fast.ai"],
                createdAt="2024-01-08T09:00:00Z",
                updatedAt="2024-01-22T13:15:00Z"
            ),
            ResearchItem(
                id="5",
                title="Genomics Analysis Pipeline",
                description="Bioinformatics pipeline for genomic sequence analysis and variant calling",
                type=ResearchItemType.REPOSITORY,
                tags=["bioinformatics", "genomics", "variant-calling", "pipeline"],
                authors=["bio-team@harvard.edu", "genomics@mit.edu"],
                createdAt="2024-01-14T11:20:00Z",
                updatedAt="2024-01-21T15:45:00Z"
            ),
            ResearchItem(
                id="6",
                title="Climate Data Collection",
                description="Historical climate data from weather stations worldwide for climate research",
                type=ResearchItemType.DATASET,
                tags=["climate", "weather", "environmental", "time-series"],
                authors=["climate@noaa.gov", "research@nasa.gov"],
                createdAt="2024-01-05T07:30:00Z",
                updatedAt="2024-01-19T12:00:00Z"
            )
        ]

    def getApiVersion(self):
        print("getApiVersion() called")
        return "Version Krish - Enhanced with Catalog Support"

    def getCatalogItems(self, filter_obj):
        print(f"getCatalogItems() called with filter: {filter_obj}")
        
        items = self.catalog_items
        
        # Apply type filter
        if filter_obj and filter_obj.type is not None:
            items = [item for item in items if item.type == filter_obj.type]
        
        # Apply search query filter
        if filter_obj and filter_obj.searchQuery:
            query = filter_obj.searchQuery.lower()
            items = [item for item in items if 
                    query in item.title.lower() or 
                    query in item.description.lower() or
                    any(query in tag.lower() for tag in item.tags)]
        
        # Apply tags filter
        if filter_obj and filter_obj.tags:
            items = [item for item in items if 
                    any(tag in item.tags for tag in filter_obj.tags)]
        
        print(f"Returning {len(items)} catalog items")
        return items

    def getResearchItem(self, item_id):
        print(f"getResearchItem() called with id: {item_id}")
        
        for item in self.catalog_items:
            if item.id == item_id:
                return item
        
        # Return None if not found (Thrift will handle this appropriately)
        return None

    def searchCatalog(self, query):
        print(f"searchCatalog() called with query: {query}")
        
        if not query:
            return self.catalog_items
        
        query_lower = query.lower()
        results = [item for item in self.catalog_items if 
                  query_lower in item.title.lower() or 
                  query_lower in item.description.lower() or
                  any(query_lower in tag.lower() for tag in item.tags) or
                  any(query_lower in author.lower() for author in item.authors)]
        
        print(f"Search returned {len(results)} results")
        return results

    def getAllTags(self):
        print("getAllTags() called")
        
        all_tags = set()
        for item in self.catalog_items:
            all_tags.update(item.tags)
        
        tags_list = sorted(list(all_tags))
        print(f"Returning {len(tags_list)} unique tags")
        return tags_list

# Extend BaseHTTPRequestHandler to add CORS headers
class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Thrift-Protocol') # X-Thrift-Protocol for TJSONProtocol
        self.send_header('Access-Control-Max-Age', '86400') # Cache preflight for 24 hours
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # Handle Thrift POST requests
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        itrans = TTransport.TMemoryBuffer(body)
        otrans = TTransport.TMemoryBuffer()
        
        iprot = TJSONProtocol.TJSONProtocol(itrans)
        oprot = TJSONProtocol.TJSONProtocol(otrans)
        
        processor.process(iprot, oprot)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/x-thrift") # Standard Thrift HTTP Content-Type
        self.send_header("Content-Length", str(len(otrans.getvalue())))
        self.end_headers()
        self.wfile.write(otrans.getvalue())

if __name__ == "__main__":
    handler = VersionServiceHandler()
    processor = VersionService.Processor(handler)
    
    # Use the custom handler with THttpServer
    # THttpServer itself uses BaseHTTPServer.HTTPServer, so we can pass our custom handler
    # Note: The THttpServer in thriftpy2 (a different library) has a make_server function that might simplify this,
    # but for Apache Thrift's official library, direct modification of BaseHTTPRequestHandler is often needed
    # for full control over headers, especially for CORS preflight.
    
    # The official Apache Thrift Python THttpServer is a bit less flexible for custom HTTP handling.
    # For a simple PoC, directly using HTTPServer with a custom RequestHandler is more robust for CORS.
    
    # Create a simple HTTP server using our custom handler
    server_address = ('localhost', 9090)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
    print(f"Starting Python Thrift server on {server_address}:{server_address[1]}...")
    httpd.serve_forever()