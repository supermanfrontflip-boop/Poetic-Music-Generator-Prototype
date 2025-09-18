import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import GenerateScreen from './screens/GenerateScreen';
import HistoryScreen from './screens/HistoryScreen';
import SongDetailScreen from './screens/SongDetailScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Generate">
        <Stack.Screen name="Generate" component={GenerateScreen} />
        <Stack.Screen name="History" component={HistoryScreen} />
        <Stack.Screen name="SongDetail" component={SongDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
