# 🌟 Outfit Orchestrator: Automating Your Wardrobe Decisions with Airflow 🚀👔👗  

Tired of wasting precious time deciding what to wear every morning? 🕒😩 Say hello to **Outfit Orchestrator**, a project that combines data engineering and fashion! Using Apache Airflow, we orchestrate the perfect outfit recommendation based on:  

- 🌦 **Weather Data:** Don't let the rain catch you off guard!  
- 📅 **Calendar Events:** Dress for every occasion.  
- 👕 **Wardrobe Inventory:** Make the most of what you own.  
- 📊 **Outfit History:** Avoid repeating looks too often.  

---

## 📖 How It Works  

### DAG Overview  
The Airflow DAG is the backbone of this project, orchestrating tasks step by step:  

1. **🧺 Load Wardrobe Inventory:**  
   Fetch data about your available clothes from a CSV file.  

2. **📖 Check Outfit History:**  
   Look back at previously worn combinations to avoid repeats.  

3. **📅 Fetch Calendar Events:**  
   Connect to your Google Calendar and retrieve today's activities.  

4. **🌦 Fetch Weather Data:**  
   Get hourly weather forecasts to plan your outfit accordingly.  

5. **👗 Generate Outfit Recommendation:**  
   Combine all the data to pick the perfect outfit for the day!  

6. **📊 Calculate Usage Statistics:**  
   Analyze which items are most frequently used and save the results to `statistics.json`.  

---

## 📈 DAG Graph  

Here's a visual overview of the DAG:  

```
    [Inventory] --> [History] --> [Calendar] --> [Weather]
                            \                 /
                             --> [Recommendation] --> [Statistics]
```  

Each node corresponds to a specific task, making the entire workflow modular, intuitive, and reusable.  

---

## 🛠 Tools Used  

- **Apache Airflow**: The orchestrator that makes everything run smoothly.  
- **Python**: The engine behind each task.  
- **Google Calendar API**: For real-time event data.  
- **OpenWeatherMap API**: For accurate weather forecasts.  
- **CSV & JSON**: For inventory and statistics storage.  


> Disclaimer: Despite all the automation, I always end up wearing the same few outfits. 😂
