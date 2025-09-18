import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function SongDetailScreen({ route }) {
  const { song } = route.params;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Song Detail</Text>
      <Text style={styles.label}>Poem:</Text>
      <Text style={styles.text}>{song.poem}</Text>
      <Text style={styles.label}>Mood:</Text>
      <Text style={styles.text}>{song.mood}</Text>

      <Button title="▶ Play" onPress={() => {}} />
      <Button title="⬇ Download" onPress={() => {}} />
      <Button title="🔁 Re-Generate" onPress={() => {}} />
      <Button title="📷 View Image" onPress={() => {}} />
      <Button title="🎵 View Reference Audio" onPress={() => {}} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  label: { fontWeight: 'bold', marginTop: 10 },
  text: { marginBottom: 10 }
});
