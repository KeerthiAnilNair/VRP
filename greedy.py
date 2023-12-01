import random
import timeit
start = timeit.default_timer()

def main():
     data=[[0, 5, 8, 6, 7, 3],  
    [5, 0, 4, 2, 7, 1],
    [8, 4, 0, 3, 6, 2], 
    [6, 2, 3, 0, 5, 2], 
    [7, 7, 6, 5, 0, 4],  
    [3, 1, 2, 2, 4, 0]]
     buses=3
     stop_capacity=[0, 4, 2, 4, 8, 8]
                  # 0, 1, 2, 3, 4, 5
    
     visited=[0]
     capacity=0
     x=0
     total_capacity=[]
     initial_sol=[]
     vect=[0]
     total_dist=[]
     dist=0
     while len(visited)<len(data):
          
          min_value=999
          for y in range(0,len(data)):
               if y not in visited and data[x][y]<min_value:
                    min_value=data[x][y]
                    index=y
          
          if capacity+stop_capacity[index]<=10:
                dist=dist+data[x][index]
                x=index
                
                capacity=capacity+stop_capacity[index]
                visited.append(index)
                vect.append(index)
          else:
              vect.append(0)
              initial_sol.append(vect)
              vect.clear
              vect=[0]
              dist=dist+data[x][0]
              total_dist.append(dist)
              dist=0
              total_capacity.append(capacity)
              capacity=0
              x=0
        #   print(vect,visited,capacity,min_value)
     total_capacity.append(capacity)
     dist=dist+data[x][0]
     total_dist.append(dist)
     vect.append(0)
     initial_sol.append(vect)
     sum=0
     for d in total_dist:
          sum=sum+d
     stop = timeit.default_timer()
     elapsed_time = stop - start
     elapsed_time_str = "{:.8f}".format(elapsed_time)
     print("\n\tGREEDY ALGORITHM\n")
     print("Optimal bus route::",initial_sol)
     print("Capacity for each bus::",total_capacity)
     print("Total distance travelled for each bus route::",total_dist)
     print("Total distance travelled of all buses::",sum)
     print("Execution Time:", elapsed_time_str, "seconds\n")
         

if __name__ == "__main__":
    main()