library(tidyverse)
library(lubridate)
library(gridExtra)
library(grid)

df = read.csv('output/output.csv')

df <- df %>%
  mutate(Date = mdy(Date))

by_Y <- df %>%
  select(Airport,Date,All.Avrg.Wait) %>%
  mutate(Year = year(Date),) %>%
  group_by(Year,Airport) %>%
  summarise(Average_wait_time = round(mean(All.Avrg.Wait),digits=2), )
by_Y

# Grouped

ggplot(by_Y, aes(fill = Airport, x=Airport, y = Average_wait_time)) +
  geom_bar(position="dodge", stat="identity") +
  facet_wrap(~Year)


ggplot(data=by_Y, aes(x=Year, y = Average_wait_time))+
  geom_bar(stat="identity",aes(fill=Year)) +
  ggtitle("Average Wait Times") +
  xlab('Airport') +
  ylab('Minutes')





by_Y_M <- df %>%
  select(Airport,Date,All.Avrg.Wait) %>%
  mutate(Year = year(Date),
         Month = month(Date)) %>%
  group_by(Year,Airport,Month) %>%
  summarise(Average_wait_time = round(mean(All.Avrg.Wait),digits=2), )
write.csv(by_Y_M, file = "output/by_Y_M.csv")

line_graph_by_Y_M<- ggplot(data = by_Y_M, mapping = aes(x = month(Month,label = TRUE), 
                                              y = Average_wait_time, 
                                              color = Airport,
                                              group = Airport,)) + 
  geom_line() +
  geom_point() +
  ggtitle("Average Wait Time Per Passenger Per Month") +
  xlab('Month') +
  ylab('Minutes')
line_graph_by_Y_M


all_around <- df %>%
  select(Airport, All.Avrg.Wait) %>%
  group_by(Airport) %>%
  summarise(Average_wait_time = round(mean(All.Avrg.Wait),digits=2), ) %>%
  arrange(Average_wait_time)

grid.table(all_around)

all_around_bar <- ggplot(data=all_around, aes(x=Airport, y = Average_wait_time))+
  geom_bar(stat="identity",aes(fill=Airport)) +
  ggtitle("Average Wait Time Per Passenger") +
  xlab('Month') +
  ylab('Minutes')




ggsave(plot = grid.table(all_around), filename = "Ranking.pdf", limitsize = FALSE, path = 'output/')
# ggsave(plot = line_graph_by_Y_M, filename = "All_months_linegraph.png",limitsize = FALSE, path = 'output/')
ggsave(plot = all_around_bar, filename = "Averages_bargraph.png",limitsize = FALSE, path = 'output/')



