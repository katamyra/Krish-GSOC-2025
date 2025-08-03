#!/usr/bin/env python3
"""
Cluster Service for CyberShuttle
Handles cluster filtering based on constraints and session startup
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Cluster:
    name: str
    max_cpus: int
    memory_gb: int
    gpu_support: str
    gpu_count: int
    jobs_in_queue: int
    owned_by: str
    cluster_type: str  # 'HPC', 'Cloud', etc.
    status: str  # 'active', 'maintenance', 'offline'

@dataclass
class SessionConstraints:
    cpu_count: int
    memory: str
    gpu_count: int
    wall_time: int

@dataclass
class SessionInfo:
    research_item: str
    cluster: str
    constraints: SessionConstraints
    dependencies: Dict[str, bool]
    storage: str
    ide: str

class ClusterService:
    def __init__(self):
        # Mock cluster data - in real implementation, this would come from a database
        self.clusters = [
            Cluster(
                name="expanse-cpu",
                max_cpus=128,
                memory_gb=256,
                gpu_support="No",
                gpu_count=0,
                jobs_in_queue=10,
                owned_by="ndeshan.b@gmail.com",
                cluster_type="HPC",
                status="active"
            ),
            Cluster(
                name="expanse-cpu-test",
                max_cpus=128,
                memory_gb=256,
                gpu_support="No",
                gpu_count=0,
                jobs_in_queue=20,
                owned_by="ndeshan.b@gmail.com",
                cluster_type="HPC",
                status="active"
            ),
            Cluster(
                name="expanse-gpu",
                max_cpus=96,
                memory_gb=192,
                gpu_support="A100 GPUs",
                gpu_count=4,
                jobs_in_queue=5,
                owned_by="ndeshan.b@gmail.com",
                cluster_type="HPC",
                status="active"
            ),
            Cluster(
                name="jetstream-cloud",
                max_cpus=64,
                memory_gb=128,
                gpu_support="V100 GPUs",
                gpu_count=2,
                jobs_in_queue=3,
                owned_by="admin@cybershuttle.org",
                cluster_type="Cloud",
                status="active"
            ),
            Cluster(
                name="bridges-cpu",
                max_cpus=256,
                memory_gb=512,
                gpu_support="No",
                gpu_count=0,
                jobs_in_queue=15,
                owned_by="admin@cybershuttle.org",
                cluster_type="HPC",
                status="maintenance"
            )
        ]

    def get_all_clusters(self) -> List[Dict[str, Any]]:
        """Get all available clusters"""
        return [self._cluster_to_dict(cluster) for cluster in self.clusters]

    def filter_clusters_by_constraints(self, constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter clusters based on user constraints
        
        Args:
            constraints: Dictionary containing cpu_count, memory, gpu_count, wall_time
            
        Returns:
            List of clusters that meet the constraints
        """
        cpu_count = constraints.get('cpu_count', 0)
        gpu_count = constraints.get('gpu_count', 0)
        # Parse memory string like "128 GB" to integer
        memory_str = constraints.get('memory', '0 GB')
        memory_needed = int(memory_str.split()[0]) if memory_str else 0
        
        filtered_clusters = []
        
        for cluster in self.clusters:
            # Skip clusters that are not active
            if cluster.status != 'active':
                continue
                
            # Check CPU constraint
            if cluster.max_cpus < cpu_count:
                logger.info(f"Cluster {cluster.name} filtered out: insufficient CPUs ({cluster.max_cpus} < {cpu_count})")
                continue
                
            # Check memory constraint
            if cluster.memory_gb < memory_needed:
                logger.info(f"Cluster {cluster.name} filtered out: insufficient memory ({cluster.memory_gb} < {memory_needed} GB)")
                continue
                
            # Check GPU constraint
            if gpu_count > 0 and cluster.gpu_count < gpu_count:
                logger.info(f"Cluster {cluster.name} filtered out: insufficient GPUs ({cluster.gpu_count} < {gpu_count})")
                continue
                
            # If we get here, cluster meets all constraints
            logger.info(f"Cluster {cluster.name} meets constraints")
            filtered_clusters.append(cluster)
            
        return [self._cluster_to_dict(cluster) for cluster in filtered_clusters]

    def _cluster_to_dict(self, cluster: Cluster) -> Dict[str, Any]:
        """Convert Cluster object to dictionary"""
        return {
            'name': cluster.name,
            'maxCPUs': cluster.max_cpus,
            'memory': f'~{cluster.memory_gb} GB',
            'gpuSupport': cluster.gpu_support,
            'jobsInQueue': cluster.jobs_in_queue,
            'ownedBy': cluster.owned_by,
            'clusterType': cluster.cluster_type,
            'status': cluster.status
        }

    def starting_session_with_info(self, session_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a session with the provided information
        This function prints session details and would normally interface with job schedulers
        
        Args:
            session_info: Dictionary containing all session configuration
            
        Returns:
            Dictionary with session startup result
        """
        timestamp = datetime.now().isoformat()
        
        # Print session info to terminal as requested
        print("\n" + "="*60)
        print("🚀 STARTING NEW CYBERSHUTTLE SESSION")
        print("="*60)
        print(f"⏰ Timestamp: {timestamp}")
        print(f"🔬 Research Item: {session_info.get('researchItem', 'Unknown')}")
        print(f"🖥️  Selected Cluster: {session_info.get('cluster', 'None')}")
        
        constraints = session_info.get('constraints', {})
        print(f"\n📊 CONSTRAINTS:")
        print(f"   💻 CPU Count: {constraints.get('cpuCount', 0)}")
        print(f"   🧠 Memory: {constraints.get('memory', 'N/A')}")
        print(f"   🎮 GPU Count: {constraints.get('gpuCount', 0)}")
        print(f"   ⏱️  Wall Time: {constraints.get('wallTime', 0)} minutes")
        
        dependencies = session_info.get('dependencies', {})
        print(f"\n📦 DEPENDENCIES:")
        print(f"   🐍 Conda: {'✅ Enabled' if dependencies.get('conda') else '❌ Disabled'}")
        print(f"   📋 Pip: {'✅ Enabled' if dependencies.get('pip') else '❌ Disabled'}")
        
        print(f"\n💾 Storage: {session_info.get('storage', 'None selected')}")
        print(f"🛠️  IDE: {session_info.get('ide', 'Not specified')}")
        
        print("\n" + "="*60)
        print("✨ Session configuration received successfully!")
        print("🔄 In a real system, this would:")
        print("   • Submit job to cluster scheduler")
        print("   • Provision compute resources")
        print("   • Setup environment with dependencies")
        print("   • Launch selected IDE")
        print("   • Mount storage volumes")
        print("="*60 + "\n")
        
        # Log to file as well
        logger.info(f"Session started: {json.dumps(session_info, indent=2)}")
        
        # Return session details
        return {
            'success': True,
            'session_id': f"session_{timestamp.replace(':', '-').replace('.', '-')}",
            'message': 'Session started successfully',
            'timestamp': timestamp,
            'session_info': session_info
        }

def main():
    """Test the cluster service"""
    service = ClusterService()
    
    # Test cluster filtering
    print("Testing cluster filtering...")
    
    # Test 1: Basic constraints
    test_constraints = {
        'cpu_count': 64,
        'memory': '128 GB',
        'gpu_count': 0,
        'wall_time': 60
    }
    
    print(f"\nTest constraints: {test_constraints}")
    filtered = service.filter_clusters_by_constraints(test_constraints)
    print(f"Clusters matching constraints: {len(filtered)}")
    for cluster in filtered:
        print(f"  - {cluster['name']}: {cluster['maxCPUs']} CPUs, {cluster['memory']}")
    
    # Test 2: GPU constraints
    gpu_constraints = {
        'cpu_count': 32,
        'memory': '64 GB',
        'gpu_count': 2,
        'wall_time': 120
    }
    
    print(f"\nGPU constraints: {gpu_constraints}")
    gpu_filtered = service.filter_clusters_by_constraints(gpu_constraints)
    print(f"GPU-capable clusters: {len(gpu_filtered)}")
    for cluster in gpu_filtered:
        print(f"  - {cluster['name']}: {cluster['gpuSupport']}")
    
    # Test session startup
    test_session = {
        'researchItem': 'ResNet-50 Image Classification',
        'cluster': 'expanse-gpu',
        'constraints': {
            'cpuCount': 32,
            'memory': '128 GB',
            'gpuCount': 2,
            'wallTime': 120
        },
        'dependencies': {
            'conda': True,
            'pip': False
        },
        'storage': '/shared/datasets/imagenet',
        'ide': 'jupyter'
    }
    
    result = service.starting_session_with_info(test_session)
    print(f"Session result: {result['message']}")

if __name__ == "__main__":
    main() 