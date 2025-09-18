import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

export default function GenerateScreen({ navigation }) {
  const [poem, setPoem] = useState('');
  const [mood, setMood] = useState('');

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Generate Song</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter your poem..."
        multiline
        value={poem}
        onChangeText={setPoem}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter mood/style..."
        value={mood}
        onChangeText={setMood}
      />
      <Button title="✨ Generate Song" onPress={() => navigation.navigate('History')} />
      <Button title="View History" onPress={() => navigation.navigate('History')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  input: { borderWidth: 1, padding: 10, marginBottom: 10, borderRadius: 5 }
});
