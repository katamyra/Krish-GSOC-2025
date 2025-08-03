// server.thrift
namespace py server_service
namespace js server_service

// Research item types
enum ResearchItemType {
    REPOSITORY = 1,
    DATASET = 2,
    MODEL = 3,
    NOTEBOOK = 4
}

// Research item structure
struct ResearchItem {
    1: string id,
    2: string title,
    3: string description,
    4: ResearchItemType type,
    5: list<string> tags,
    6: list<string> authors,
    7: string createdAt,
    8: string updatedAt
}

// Catalog filter options
struct CatalogFilter {
    1: optional ResearchItemType type,
    2: optional list<string> tags,
    3: optional string searchQuery
}

service VersionService {
    string getApiVersion()
    
    // Catalog methods
    list<ResearchItem> getCatalogItems(1: CatalogFilter filter),
    ResearchItem getResearchItem(1: string itemId),
    list<ResearchItem> searchCatalog(1: string query),
    list<string> getAllTags()
} 