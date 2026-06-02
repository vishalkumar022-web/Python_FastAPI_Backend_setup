# yaha through DTOs file ham apne data transfer objects ko define karenge jo ki client aur server ke beech data transfer ke liye use honge. In DTOs ko hum Pydantic models ke through define karenge, jisse hum apne data ko validate kar sakte hain aur ensure kar sakte hain ki data expected structure ke according hai. In DTOs me hum apne task data ke fields ko define karenge, jaise ki title, description, status, aur due_date. Isse hum apne application me task data ko easily manage kar sakte hain aur client se aane wale data ko validate karke ensure kar sakte hain ki wo sahi format me hai. Overall, yeh DTOs file hamare application ke liye ek important role play karegi in terms of data validation and structuring for task-related operations.



from pydantic import BaseModel # yaha hum Pydantic ke BaseModel ko import kar rahe hain, jisse hum apne DTOs ko define kar sakte hain. Pydantic ke BaseModel ka use karke hum apne data transfer objects ko easily define kar sakte hain aur unhe validate kar sakte hain. Isse hum apne application me data validation ko ensure kar sakte hain aur client se aane wale data ko expected structure ke according validate kar sakte hain.

class TaskDTO(BaseModel): # yaha hum apne TaskDTO ko define kar rahe hain, jisme hum apne task data ke fields ko specify karenge. Is DTO me hum title, description, status, aur due_date fields ko define karenge, jisse hum apne application me task data ko easily manage kar sakte hain aur client se aane wale data ko validate karke ensure kar sakte hain ki wo sahi format me hai. Is DTO ka use karke hum apne application me task-related operations ke liye data validation aur structuring ko ensure kar sakte hain.
    title: str
    description: str
    status: bool = False

    
 
