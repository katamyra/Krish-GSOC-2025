package org.apache.airavata.admin_api_server.entity;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import java.util.List;

@Entity
@Table(name = "notebooks")
public class Notebook {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String title;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "notebook_tags", joinColumns = @JoinColumn(name = "notebook_id"))
    @Column(name = "tag")
    private List<String> tags;
    
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "notebook_authors", joinColumns = @JoinColumn(name = "notebook_id"))
    @Column(name = "author")
    private List<String> authors;
    
    private String category;
    
    // Constructors
    public Notebook() {}
    
    public Notebook(String title, String description, List<String> tags, List<String> authors, String category) {
        this.title = title;
        this.description = description;
        this.tags = tags;
        this.authors = authors;
        this.category = category;
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public List<String> getTags() { return tags; }
    public void setTags(List<String> tags) { this.tags = tags; }
    
    public List<String> getAuthors() { return authors; }
    public void setAuthors(List<String> authors) { this.authors = authors; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
}