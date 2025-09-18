import React from 'react';
import { View, Text, FlatList, Button, StyleSheet } from 'react-native';

const dummySongs = [
  { id: '1', poem: 'The stars are dancing...', mood: 'dreamy' },
  { id: '2', poem: 'A river flows...', mood: 'calm' }
];

export default function HistoryScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>History</Text>
      <FlatList
        data={dummySongs}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.poem}>{item.poem}</Text>
            <Text style={styles.mood}>Mood: {item.mood}</Text>
            <Button title="▶ Play" onPress={() => {}} />
            <Button title="⬇ Download" onPress={() => {}} />
            <Button title="🔁 Re-Generate" onPress={() => {}} />
            <Button title="Details" onPress={() => navigation.navigate('SongDetail', { song: item })} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: { padding: 15, borderWidth: 1, borderRadius: 8, marginBottom: 10 },
  poem: { fontSize: 16, marginBottom: 5 },
  mood: { fontSize: 14, marginBottom: 10, color: 'gray' }
});
