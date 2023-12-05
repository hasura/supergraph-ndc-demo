export function helloWorld(): string {
    return "Hello world";
};

export function addNumbers(a: number, b: number): number {
    return a + b;
};

export function isEven(num: number): boolean {
    return num % 2 === 0;
};

export function stringLength(str: string): number {
    return str.length;
};

export function containsElement<T>(arr: T[], element: T): boolean {
    return arr.includes(element);
};

export function generateRange(start: number, end: number): number[] {
    if (start > end) {
        throw new Error("Start must be less than end");
    }
    const list: number[] = [];
    for (let i = start; i <= end; i++) {
        list.push(i);
    }
    return list;
}

export type CatFact = {
    fact: string;
    length: number;
}

export async function fetchCatFacts(page: number, max_length: number, limit: number): Promise<any> {
    try {
        const url = `https://catfact.ninja/facts?page=${page}&max_length=${max_length}&limit=${limit}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        const factResponse: CatFact[] = jsonResponse.data as CatFact[];
        return factResponse;
    } catch (error) {
        console.error('Error fetching cat facts:', error);
        throw error;
    }
}

export type DadJoke = {
    id: string;
    joke: string;
    status: number;
}

export async function fetchRandomDadJoke(): Promise<any> {
    try {
        const response = await fetch('https://icanhazdadjoke.com/', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'Hasura Graph Demo' // Replace with your actual User-Agent
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const joke: DadJoke = await response.json();
        console.log(joke);
        return joke;
    } catch (error) {
        console.error('Error fetching a random dad joke:', error);
        throw error;
    }
}


export async function defineWord(word: string): Promise<string> {
    try {
        const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`, {
            method: 'GET'
        });

        if (!response.ok) {
            return "There was an error fetching the definition.";
        }

        const data = await response.json();
        // Assuming the first meaning and first definition are desired
        const definition: string = data[0].meanings[0].definitions[0].definition;
        return definition;
    } catch (error) {
        return error.toString();
    }
}
