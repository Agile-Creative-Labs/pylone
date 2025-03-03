/**
 * LRUCache Class
 *
 * Implements a Least Recently Used (LRU) cache with a specified capacity.
 * The cache evicts the least recently used item when adding a new item if the capacity is exceeded.
 *
 * @author Agile Creative Labs Inc.
 * @date 2025-03-02
 * @version 1.0.0
 *
 * Usage Example:
 *
 * // Initialize the cache with a capacity of 3
 * const cache = new LRUCache(3);
 *
 * // Add items to the cache
 * cache.put("A", 1);
 * cache.put("B", 2);
 * cache.put("C", 3);
 *
 * // Retrieve an item
 * console.log(cache.get("A")); // Output: 1
 *
 * // Add a new item, causing "B" to be evicted
 * cache.put("D", 4);
 * console.log(cache.get("B")); // Output: null
 *
 * // Resize the cache to a capacity of 2
 * cache.resize(2);
 * console.log(cache.get("C")); // Output: null
 */
class LRUCache {
    constructor(capacity) {
      if (capacity <= 0) {
        throw new Error("Capacity must be greater than zero");
      }
      this.capacity = capacity;
      this.cache = new Map();
    }
  
    /**
     * Retrieves an item from the cache.
     *
     * @param {string} key - The key of the item to retrieve.
     * @returns {*} - The value of the item, or null if the item does not exist.
     */
    get(key) {
      if (!this.cache.has(key)) {
        return null;
      }
      const value = this.cache.get(key);
      // Refresh the key by deleting and setting it again
      this.cache.delete(key);
      this.cache.set(key, value);
      return value;
    }
  
    /**
     * Adds an item to the cache.
     *
     * @param {string} key - The key under which to store the value.
     * @param {*} value - The value to store.
     */
    put(key, value) {
      if (key == null || value == null) {
        throw new Error("Key and value cannot be null");
      }
      if (this.cache.size >= this.capacity && !this.cache.has(key)) {
        // Evict the least recently used item
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
      // Refresh the key by deleting it if it exists
      if (this.cache.has(key)) {
        this.cache.delete(key);
      }
      this.cache.set(key, value);
    }
  
    /**
     * Clears all items from the cache.
     */
    clear() {
      this.cache.clear();
    }
  
    /**
     * Resizes the cache to a new capacity.
     *
     * @param {number} newCapacity - The new capacity of the cache.
     */
    resize(newCapacity) {
      if (newCapacity <= 0) {
        throw new Error("New capacity must be greater than zero");
      }
      this.capacity = newCapacity;
      while (this.cache.size > newCapacity) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
    }
  }
  
  // Example usage
  const cache = new LRUCache(3);
  cache.put("A", 1);
  cache.put("B", 2);
  cache.put("C", 3);
  console.log(cache.get("A")); // Output: 1
  cache.put("D", 4); // "B" is evicted
  console.log(cache.get("B")); // Output: null
  console.log(cache.get("C")); // Output: 3
  console.log(cache.get("D")); // Output: 4
  
  // Resize the cache
  cache.resize(2); // "C" is evicted
  console.log(cache.get("C")); // Output: null
  