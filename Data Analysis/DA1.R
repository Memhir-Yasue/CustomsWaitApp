library(tidyverse)
library(lubridate)
library(gridExtra)
library(grid)


df = read.csv('output.csv')

df <- df %>%
  mutate(Date = mdy(Date),
         Day_of_week = wday(Date, label = TRUE, abbr = TRUE),
         Month = month(Date, label = TRUE))

df_2018 <- df %>%
  filter(year(Date) == 2018)

days_in_months = 31 + 28 + 31

summer <- df_2018 %>%
 filter( (Month == 'Jan' | Month == 'Feb' | Month == 'Mar') ) %>%
  group_by(Airport,Hour) %>%
  select(Airport,Hour,All.Avrg.Wait, Total, Flights) %>%
  summarise(
    Average_wTime_per_Pax = round(sum(All.Avrg.Wait)/days_in_months,1),
    Average_flights = round(sum(Flights)/days_in_months,1),
    Average_pax = round(sum(Total)/days_in_months,1),
  )


by_dayOf_week <- df_2018 %>%
  group_by(Airport,Day_of_week) %>%
  select(Airport, Day_of_week,All.Avrg.Wait, Total, Flights, Booths) %>%
  summarise(
            Average_wTime_per_Pax = round(mean(All.Avrg.Wait),1),
            Average_num_Pax = round(sum(Total)/52,1),
            Average_num_Flights = round(sum(Flights)/52,1),
            Average_num_booth = round(mean(Booths),1),
            )

by_Hour <-df_2018 %>%
  group_by(Airport,Hour) %>%
  select(Airport, Hour,All.Avrg.Wait, Total, Flights, Booths) %>%
  summarise(
    Average_wTime_per_Pax = round(mean(All.Avrg.Wait),1),
    Average_num_Pax = round(mean(Total),1),
    Average_num_Flights = round(mean(Flights),1),
    Average_num_booth = round(median(Booths),1), )

by_Hour_n_DayofWeek <- df_2018 %>%
  group_by(Airport,Day_of_week,Hour) %>%
  select(Airport,Day_of_week,Hour,All.Avrg.Wait, Total, Flights, Booths) %>%
  summarise(
    Average_wTime_per_Pax = round(mean(All.Avrg.Wait),1),
    Average_num_Pax = round(sum(Total),1),
    Average_num_Flights = round(sum(Flights)/52,1),
    Average_num_booth = round(mean(Booths),1),
  )

by_Hour_n_DayofWeek_n_month <- df_2018 %>%
  group_by(Airport,Month,Day_of_week,Hour) %>%
  select(Airport, Month,Day_of_week,Hour,All.Avrg.Wait, Total, Flights, Booths) %>%
  summarise(
    Average_wTime_per_Pax = round(mean(All.Avrg.Wait),1),
    Average_num_Pax = round(mean(Total),1),
    Average_num_Flights = round(mean(Flights),1),
    Average_num_booth = round(mean(Booths),1),
  ) 

graph_bar <- function(data,x,y,xlabel,ylabel) {
  ggplot(data=data,aes(x = x, y = y, color = Airport)) +
    geom_bar(aes(fill=Airport),position="dodge", stat="identity") +
    # xlab("Day of the Week") +
    # ylab("Average Waiting Time Per Passenger") +
    facet_wrap(~Airport) +
    theme(axis.text.x = element_text(angle=90)) +
    xlab(xlabel)+
    ylab(ylabel)
    
}
#graph_bar(by_Hour,by_Hour$Hour,by_Hour$Average_wTime_per_Pax)
graph_bar(summer,summer$Hour,summer$Average_wTime_per_Pax,"Hour","Wait Time")
graph_bar(summer,summer$Hour,summer$Average_pax,"Hour","Num of pax")
graph_bar(summer,summer$Hour,summer$Average_flights,"Hour","Num of flights")
write.csv(by_Hour, file = "by_Hour.csv")

 ggplot(data=by_dayOf_week,aes(x = Day_of_week, y = Average_wTime_per_Pax, color = Airport)) +
   geom_line(aes(group=Airport)) +
   geom_point() +
   xlab("Day of the Week") +
   ylab("Average Waiting Time Per Passenger Per Flight")
 
 
 ggplot(data=by_dayOf_week,aes(x = Day_of_week, y = Average_num_Pax, color = Airport)) +
   geom_line(aes(group=Airport)) +
   geom_point() +
   xlab("Day of the week") +
   ylab("Average Number of International Passengers (Inbound) Per Day of Week")
 
 ggplot(data=by_dayOf_week,aes(x = Day_of_week, y = Average_num_Flights, color = Airport)) +
   geom_line(aes(group=Airport)) +
   geom_point() +
   xlab("Day of the week") +
   ylab("Average Number of International Flights (Inbound) Per Day of Week")
 
 ggplot(data=by_dayOf_week,aes(x = Day_of_week, y = Average_num_booth, color = Airport)) +
   geom_line(aes(group=Airport)) +
   geom_point() +
   xlab("Day of the week") +
   ylab("Average number of Customs Booth per Flight")
   #geom_bar(aes(fill=Airport),position="dodge", stat="identity")